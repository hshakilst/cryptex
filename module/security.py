#!/usr/bin/python
import base64
import csv

from Crypto import Random
from Crypto.PublicKey import RSA

from module import crypto, csv_query

db_faculties = './database/faculties.csv'
db_courses = './database/courses.csv'
db_pub_keys = './key_server/keys.csv'
db_uid = './key_server/uid.csv'
db_user_keys = './key_server/user_keys.csv'

def top_secret_encrypt(fname, users, confidentiality):
    doc_key, hash_of_encf = crypto.aes_file_encrypt(fname)
    key1 = Random.new().read(64)
    file_uid = open(db_uid, 'rb')
    reader_uid = csv.reader(file_uid, delimiter = '\t')
    file_pub_key = open(db_pub_keys, 'rb')
    reader_pub_key = csv.reader(file_pub_key, delimiter = '\t')
    file_user_keys = open(db_user_keys,'ab')
    writer = csv.writer(file_user_keys, delimiter = '\t')
    for user in users:
        # result = csv_query.query("select uuid from "+db_uid+" where id='"+user.id+"'")
        file_uid.seek(0)
        key2 = crypto.aes_iv_encrypt(doc_key, key1, (row[1] for row in reader_uid if row[0] == user.id).strip())
        # pub_key = csv_query.query("select public_key from "+db_pub_keys+" where id='"+user.id+"'")
        file_pub_key.seek(0)
        key3 = crypto.rsa_encrypt(key2+'#'+key1, RSA.importKey((row[1] for row in reader_pub_key if row[0] == user.id).strip()))
        f = fname.strip().split('/')
        r = []
        r.append(f[len(f) - 1])
        r.append(hash_of_encf)
        r.append(user.id)
        r.append(confidentiality)
        r.append(key3)
        writer.writerow(r)
    file_uid.close()
    file_pub_key.close()
    file_user_keys.close()


        

def top_secret_decrypt(fname, key3, uuid, private_key):
    key = (base64.urlsafe_b64decode(crypto.rsa_decrypt(key3, RSA.importKey(private_key)))).split('#')
    doc_key = crypto.aes_iv_decrypt(key[0], key[1], uuid)
    if(doc_key == ''):
        print "Key derivation unsuccessful!"
        return False
    else:
        flag = crypto.aes_file_decrypt(fname, doc_key)
        print "File decrypted successfully!"
        return flag

def confidential_encrypt(fname, users, confidentiality):
    doc_key, hash_of_encf = crypto.aes_file_encrypt(fname)
    file_pub_keys = open(db_pub_keys,'rb')
    file_user_keys = open(db_user_keys,'ab')
    writer = csv.writer(file_user_keys, delimiter = '\t')
    reader = csv.reader(file_pub_keys, delimiter = '\t')
    global key1
    for user in users:
        # key1 = crypto.rsa_encrypt(doc_key, RSA.importKey(row[1] for row in reader if(user.id == row[0])))
        for row in reader:
            if(user.id == row[0]):
                r = []
                key1 = crypto.rsa_encrypt(doc_key, RSA.importKey(row[1]))
                f = fname.strip().split('/')
                r.append(f[len(f) - 1])
                r.append(hash_of_encf)
                r.append(user.id)
                r.append(confidentiality)
                r.append(key1)
                writer.writerow(r)
                break
        file_pub_keys.seek(0)
    file_pub_keys.close()
    file_user_keys.close()
            
    # for pub_key in pub_keys:
        # pub_key = csv_query.query("select public_key from "+db_keys+" where id='"+user.id+"'")

def confidential_decrypt(fname, key, private_key):
    file = open(private_key, 'rb')
    doc_key = crypto.rsa_decrypt(key, RSA.importKey(file.readlines()))
    if(doc_key == ''):
        print "Key derivation unsuccessful!"
        return False
    else:
        flag = crypto.aes_file_decrypt(fname, doc_key)
        print "File decrypted successfully!"
        return flag
