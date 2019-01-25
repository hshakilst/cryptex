#!/usr/bin/python
from module import crypto
import csv

def generate_keys_all():
    db_teachers = open('./database/faculties.csv', 'rb')
    key_server = open('./key_server/keys.csv', 'wb')
    writer = csv.writer(key_server, delimiter='\t')
    reader = csv.reader(db_teachers, delimiter='\t')
    for row in reader:
        r = []
        r.append(row[3])
        private_key, public_key = crypto.genrate_keys_rsa()
        r.append(public_key)
        writer.writerow(r)
        file = open('./private_keys/'+ row[3] + '.private', 'wb')
        file.writelines(private_key)
        file.close()
    db_teachers.close()
    key_server.close()

