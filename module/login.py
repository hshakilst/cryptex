#!/usr/bin/python
import csv
from Crypto import Random
from Crypto.PublicKey import RSA
from module import crypto
from module.user import User

db_faculties = './database/faculties.csv'
key_server = './key_server/keys.csv'


def login(uid, private_key):
    file = open(key_server)
    private_key = open(private_key, 'rb').readlines()
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        if row[0].strip() == uid:
            challenge = Random.new().read(32)
            cipher = crypto.rsa_encrypt(challenge, RSA.importKey(row[1]))
            decipher = crypto.rsa_decrypt(cipher, RSA.importKey(private_key))
            if challenge == decipher:
                file = open(db_faculties)
                reader = csv.reader(file, delimiter='\t')
                for row in reader:
                    if row[3] == uid:
                        user = User(row[0], row[1], row[2], row[3], row[4])
                        return user
                    else:
                        continue
                return User()
            else:
                print 'login failed!'
        else:
            continue