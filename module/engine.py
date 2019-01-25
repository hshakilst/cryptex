#!/usr/bin/python
from module import keyword_classifier
from module import csv_query
from module.user import User
from module import security
from module import crypto
from module import keywords

db_faculties = './database/faculties.csv'
db_courses = './database/courses.csv'
db_keys = './key_server/keys.csv'
db_uid = './key_server/uid.csv'

def get_list(keywords):
    position = []
    courses = []
    department = []
    for key in keywords:
        key = key.strip()
        label = keyword_classifier.predict_label(key)
        if (label == ''):
            pass
        elif(label == 'position'):
            results = csv_query.query(
                "select * from " + db_faculties + " where position like '%"+key.replace(' ', '%')+"%'")
            lines = results.split('\n')
            for line in lines:
                fields = line.split('\t')
                user = User(fields[0].strip(), fields[1].strip(
                ), fields[2].strip(), fields[3].strip(), fields[4].strip())
                position.append(user)
        elif(label == 'course'):
            results = csv_query.query(
                "select * from " + db_courses + " where courses like '%"+key.replace(' ', '%')+"%'")
            lines = results.split('\n')
            for line in lines:
                fields = line.split('\t')
                ids = fields[2].strip().split(',')
                for id in ids:
                    results = csv_query.query(
                        "select * from " + db_faculties + " where id = '"+id+"'")
                    fields = results.split('\t')
                    user = User(fields[0].strip(), fields[1].strip(
                    ), fields[2].strip(), fields[3].strip(), fields[4].strip())
                    courses.append(user)
        elif(label == 'department'):
            results = csv_query.query(
                "select * from " + db_faculties + " where department like '%"+key.replace(' ', '%')+"%'")
            lines = results.split('\n')
            for line in lines:
                fields = line.split('\t')
                user = User(fields[0].strip(), fields[1].strip(
                ), fields[2].strip(), fields[3].strip(), fields[4].strip())
                department.append(user)
        else:
            pass
    return position, courses, department

def get_users(keywords, logged_in_user, filter = None):
    position, courses, department = get_list(keywords)
    if (filter == None) :
        if((len(position) != 0) and (len(courses) != 0) and (len(department) != 0)):
            users = list(set(position) | set(courses) | set(department))
            users.append(logged_in_user)
            return list(set(users))
        else:
            if((len(position) != 0) and (len(courses) != 0)):
                users = list(set(position) | set(courses))
                users.append(logged_in_user)
                return list(set(users))
            elif((len(courses) != 0) and (len(department) != 0)):
                users = list(set(courses) | set(department))
                users.append(logged_in_user)
                return list(set(users))
            elif((len(position) != 0) and (len(department) != 0)):
                users = list(set(position) | set(department))
                users.append(logged_in_user)
                return list(set(users))
            elif(len(position) != 0):
                users = position
                users.append(logged_in_user)
                return list(set(users))
            elif(len(courses) != 0):
                users = courses
                users.append(logged_in_user)
                return list(set(users))
            elif(len(department) != 0):
                users = department
                users.append(logged_in_user)
                return list(set(users))
            else:
                users = []
                users.append(logged_in_user)
                return list(set(users))
    else:
        p, c, d = get_list(filter)
        filter = list(set(p) | set(c) | set(d))
        if((len(position) != 0) and (len(courses) != 0) and (len(department) != 0)):
            users = list(set(position) | set(courses) | set(department))
            users = list(set(users) & set(filter))
            users.append(logged_in_user)
            return list(set(users))
        else:
            if((len(position) != 0) and (len(courses) != 0)):
                users = list(set(position) | set(courses))
                users = list(set(users) & set(filter))
                users.append(logged_in_user)
                return list(set(users))
            elif((len(courses) != 0) and (len(department) != 0)):
                users = list(set(courses) | set(department))
                users = list(set(users) & set(filter))
                users.append(logged_in_user)
                return list(set(users))
            elif((len(position) != 0) and (len(department) != 0)):
                users = list(set(position) | set(department))
                users = list(set(users) & set(filter))
                users.append(logged_in_user)
                return list(set(users))
            elif(len(position) != 0):
                users = position
                users = list(set(users) & set(filter))
                users.append(logged_in_user)
                return list(set(users))
            elif(len(courses) != 0):
                users = courses
                users = list(set(users) & set(filter))
                users.append(logged_in_user)
                return list(set(users))
            elif(len(department) != 0):
                users = department
                users = list(set(users) & set(filter))
                users.append(logged_in_user)
                return list(set(users))
            else:
                users = []
                users = list(set(users) & set(filter))
                users.append(logged_in_user)
                return list(set(users))



def engine_encrypt(fname, confidentiality, keyword, logged_in_user):
    users = get_users(keyword, logged_in_user)
    if(confidentiality == 'top secret'):
       security.top_secret_encrypt(fname, users, confidentiality)
    elif(confidentiality == 'confidential'):
       security.confidential_encrypt(fname, users, confidentiality)
    else:
        pass
    
def engine_add_keywords(fname, confidentiality, keyword, logged_in_user):
    users = get_users(keyword, logged_in_user)
    u = []
    for user in users:
        u.append(user.id)
    properties = {"author" : logged_in_user.name, 
    "confidentiality": confidentiality, 
    "authenticity" : crypto.gen_hash_file(fname), "users" : u}
    keywords.add_keywords(fname, properties)

def engine_view_keywords(fname):
    keys = keywords.read_keywords(fname)
    print "author: " + keys['author']
    print "confidentiality: " + keys['confidentiality']
    print "authenticity: " + keys['authenticity']
    print "users: " + str(keys['users'])

def engine_decrypt(fname, confidentiality, key, private_key, uuid=None ):
    if(confidentiality == 'top secret'):
        security.top_secret_decrypt(fname, key, uuid, private_key)
    elif(confidentiality == 'confidential'):
        security.confidential_decrypt(fname, key, private_key)
    else:
        pass
