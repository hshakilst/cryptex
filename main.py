#!/usr/bin/python

import sys
from module import engine
from module import keywords as Keywords
from module.user import User
from module import csv_query
from module import crypto
from module import login
import base64
import glob
import csv
import time
import json
import ast

def banner():    
    print '---------------------------------------------------------------------------------------'
    print '| |---------------------------------------------------------------------------------| |'
    print '| |   .d8888b.  8888888b. Y88b   d88P 8888888b. 88888888888 8888888888 Y88b   d88P  | |'
    print '| |  d88P  Y88b 888   Y88b Y88b d88P  888   Y88b    888     888         Y88b d88P   | |'
    print '| |  888    888 888    888  Y88o88P   888    888    888     888          Y88o88P    | |'
    print '| |  888        888   d88P   Y888P    888   d88P    888     8888888       Y888P     | |'
    print '| |  888        8888888P"     888     8888888P"     888     888           d888b     | |'
    print '| |  888    888 888 T88b      888     888           888     888          d88888b    | |'
    print '| |  Y88b  d88P 888  T88b     888     888           888     888         d88P Y88b   | |'
    print '| |   "Y8888P"  888   T88b    888     888           888     8888888888 d88P   Y88b  | |'
    print '| |---------------------------------------------------------------------------------| |'
    print '---------------------------------------------------------------------------------------'                                                                          
    print '\n'                                                                         

def root_menu(logged_in_user):
    banner()
    print '1) Upload File'
    print '2) Download File'
    print '3) Read File Metadata'
    print '4) File Directory'
    print '5) Generate Key'
    print '6) User Info'
    print '7) Log Out'
    print '8) Exit'
    print '\n'
    
    i = input('cryptex>')

    if (i == 1):
        upload_file(logged_in_user)
    elif (i == 2):
        decrypt_file(logged_in_user)
    elif (i == 3):
        file_path = raw_input('Path>')
        engine.engine_view_keywords(file_path)
    elif (i == 4):
        file_dir(logged_in_user)
    elif (i == 5):
        generate_key(logged_in_user)
    elif (i == 6):
        user_info(logged_in_user)
    elif (i == 7):
        log_out(logged_in_user)
    elif (i == 8):
        sys.exit(0)
    else:
        print "Invalid Syntax!"
    root_menu(logged_in_user)

def upload_file(logged_in_user):
    banner()
    print '1) Set File Path'
    print '2) Show File Path'
    print '3) Set Confidentiality(top secret/confidential/public'
    print '4) Show Confidentiality'
    print '5) Set Keywords(CSV Format)'
    print '6) View Keywords'
    print '7) Set Filters(CSV Format)'
    print '8) View Filters'
    print '9) Show Receiving Person(s)'
    print '10) Write metadata to file'
    print '11) View metadata of the file'
    print '12) Upload Now'
    print '13) Back'
    print '14) Exit'
    print '\n'

    i = input('cryptex>')

    global fname
    global confidentiality
    global keys
    global keywords
    global filters
    global filter
    if (i == 1):
        fname = raw_input('Path>')
    elif (i == 2):
        print fname
    elif (i == 3):
        confidentiality = raw_input('Confidentiality>')  
    elif (i == 4):
        print confidentiality
    elif (i == 5):
        keywords = raw_input('Keywords>')
        keys = keywords.strip().split(',')
    elif (i == 6):
        print keywords
    elif (i == 7):
        filters = raw_input('Filters>')
        filter = filters.strip().split(',')
    elif (i == 8):
        print filters
    elif (i == 9):
        if(type(filter) is list):
            users = engine.get_users(keys, logged_in_user, filter)
            print 'User' + '\t' + 'ID'
            print '--------------------------'
            for user in users: print user.name + '\t' + user.id
        else:    
            users = engine.get_users(keys, logged_in_user)
            print 'User' + '\t' + 'ID'
            print '--------------------------'
            for user in users: print user.name + '\t' + user.id
    elif (i == 10):
        engine.engine_add_keywords(fname, confidentiality, keys, logged_in_user)
    elif (i == 11):
        engine.engine_view_keywords(fname)
    elif (i == 12):
        engine.engine_encrypt(fname, confidentiality, keys, logged_in_user)
    elif (i == 13):
        root_menu(logged_in_user)
    elif (i == 14):
        sys.exit(0)
    else:
        print "Invalid Syntax!"
    upload_file(logged_in_user)

def decrypt_file(logged_in_user):
    banner()
    print '1) Set File Path'
    print '2) Show File Path'
    print '3) Decrypt Now'
    print '4) Back'
    print '5) Exit'
    print '\n'
    
    i = input('cryptex>')

    global fname
    global keys

    if (i == 1):
        fname = raw_input('Path>')
    elif (i == 2):
        print fname
    elif (i == 3):
        key = ''
        confidentiality = ''
        uuid = csv_query.query("select uuid from ./key_server/uid.csv where id='"+logged_in_user.id+"'")
        private_key = './private_keys/' + logged_in_user.id + '.private'
        file_user_keys = open('./key_server/user_keys.csv', 'rb')
        reader = csv.reader(file_user_keys, delimiter = '\t')
        hash_of_encf = crypto.gen_hash_file(fname)
        for row in reader:
            if(row[1] == hash_of_encf and row[2] == logged_in_user.id):
                    confidentiality = row[3]
                    key = row[4]
        if(key == ''):
            print "Keys not found!"
        else:
            engine.engine_decrypt(fname, confidentiality, key, private_key, uuid)
            file_user_keys.close()
    elif (i == 4):
        root_menu(logged_in_user)
    elif (i == 5):
        sys.exit(0)
    else:
        print "Invalid Syntax!"
    decrypt_file(logged_in_user)

def file_dir(logged_in_user):
    banner()
    print '1) Show All Files'
    print '2) Search File'
    print '3) Back'
    print '4) Exit'
    print '\n'

    i = input('cryptex>')

    enc_files = glob.glob('./ftp_server/encrypted_file/*.*')
    dec_files = glob.glob('./ftp_server/decrypted_file/*.*')

    if (i == 1):
        print 'Encrypted Files:'
        print '---------------'
        file_user_keys = open('./key_server/user_keys.csv', 'rb')
        reader = csv.reader(file_user_keys, delimiter = '\t')
        for row in reader:
            if(row[2] == logged_in_user.id):
                print "File Name: " + row[0]
                print "File Hash: " + row[1]
                print "Confidentiality: " + row[3]

        print 'Decrypted Files:'
        print '---------------'
        i = 1
        for file in dec_files:
            f = file.strip().split('/')
            print str(i)+') '+ f[len(f)-1]
            i+=1

    elif (i == 2):
        search_key = raw_input("Search Keywords>")
        matching = [(file.strip().split('/'))[len(file.strip().split('/')) -1] for file in enc_files if search_key in file]
        print 'File Found:'
        print '-----------'
        i = 1
        for file in matching:
            print str(i) + file
            i+=1
            
    elif (i == 3):
        root_menu(logged_in_user)
    elif (i == 4):
        sys.exit(0)
    else:
        print "Invalid Syntax!"
    file_dir(logged_in_user)

def user_info(logged_in_user):
    banner()
    print 'User Information:\n'
    print 'ID: ' + logged_in_user.id
    print 'Name: ' + logged_in_user.name
    print 'Email: ' + logged_in_user.email
    print 'Department: ' + logged_in_user.department
    print 'Position: ' + logged_in_user.position
    print '\n1) Back'
    print '2) Exit'
    print '\n'

    i = input('cryptex>')

    if (i == 1):
        root_menu(logged_in_user)
    elif (i == 2):
        sys.exit(0)
    user_info(logged_in_user)

def generate_key(logged_in_user):
    banner()
    print 'Generated Keys:\n'
    private_key, public_key = crypto.genrate_keys_rsa()
    print 'Private Key:'
    print private_key+'\n'
    print 'Public Key:'
    print public_key

    file = open(logged_in_user.id + '.private', 'wb')
    file.writelines(private_key)

    input_file = open('./key_server/keys.csv', 'rb')
    output_file = open('./key_server/keys.csv', 'wb')
    all = []
    reader = csv.reader(input_file, delimiter='\t')
    writer = csv.writer(output_file, delimiter='\t')
    for row in reader:
        a = []
        if(logged_in_user.id == row[0]):
            a.append(row[0])
            a.append(public_key)
        else:
            a.append(row[0])
            a.append(row[1])
        all.append(a)
    writer.writerows(all)
    input_file.close()
    output_file.close()


    print '\n1) Back'
    print '2) Exit'
    print '\n'

    i = input('cryptex>')

    if (i == 1):
        root_menu(logged_in_user)
    elif (i == 2):
        sys.exit(0)
    generate_key(logged_in_user)

def log_out(logged_in_user):
    logged_in_user = User()
    print 'User Succesfully Logged Out!'
    main()

def log_in():
    banner()
    print 'Login:\n'
    uid = raw_input('ID>')
    private_key = raw_input('Private Key Path>')
    logged_in_user = login.login(uid, private_key)
    return logged_in_user

def main():
    logged_in_user = log_in()
    if(logged_in_user.id == ''):
        time.sleep(3)
        log_in()
    else:
        root_menu(logged_in_user)

main()
        