#!/usr/bin/python

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import hashlib
import base64
import csv
import magic

# Initialization Vector For Randomizing Pattern For Makng It Hard For Rainbow Table Attack
# We Hashed Initial Vector With MD5 Hash Algorithm For Acquiring 16 byte Size of IV

# Salt Size
SALT_SIZE = 16

# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 20

# the size multiple required for AES
AES_MULTIPLE = 16

def generate_key_aes(password, salt, iterations):
    assert iterations > 0
    key = password + salt
    for i in range(iterations):
        key = hashlib.sha256(key).digest()
    return key


def pad_text(text, multiple):
    extra_bytes = len(text) % multiple
    padding_size = multiple - extra_bytes
    padding = chr(padding_size) * padding_size
    padded_text = text + padding
    return padded_text


def unpad_text(padded_text):
    padding_size = ord(padded_text[-1])
    text = padded_text[:-padding_size]
    return text


def aes_iv_encrypt(plaintext, password, IV):
    IV = hashlib.md5(IV).digest()
    salt = Random.new().read(SALT_SIZE)
    key = generate_key_aes(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_CBC, IV)
    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    return base64.urlsafe_b64encode(ciphertext_with_salt)


def aes_iv_decrypt(ciphertext, password, IV):
    ciphertext = base64.urlsafe_b64decode(ciphertext)
    IV = hashlib.md5(IV).digest()
    salt = ciphertext[0:SALT_SIZE]
    ciphertext_sans_salt = ciphertext[SALT_SIZE:]
    key = generate_key_aes(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_CBC, IV)
    padded_plaintext = cipher.decrypt(ciphertext_sans_salt)
    plaintext = unpad_text(padded_plaintext)
    return plaintext


def aes_file_encrypt(fname):
    path = fname.split('/')
    name = ''
    for s in path:
        name = s
    raw_file = open(fname,'rb')
    encrypted_file = open('./ftp_server/encrypted_file/'+name+'.enc', 'wb')
    password = base64.urlsafe_b64encode(Random.new().read(64))
    IV = Random.new().read(AES.block_size)
    salt = Random.new().read(SALT_SIZE)
    key = generate_key_aes(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_CBC, IV)
    padded_plaintext = pad_text(raw_file.read(), AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    encrypted_file.write(IV+salt+ciphertext)
    raw_file.close()
    encrypted_file.close()
    hash_encf = gen_hash_file(encrypted_file.name)
    return password, hash_encf


def aes_file_decrypt(fname, password):
    path = fname.split('/')
    name = ''
    for s in path:
        name = s
    encrypted_file = open(fname)
    raw_file = open('./ftp_server/decrypted_file/'+name.replace('.enc',''), 'wb')
    ciphertext = encrypted_file.read()
    IV = ciphertext[0:AES.block_size]
    salt = ciphertext[AES.block_size:SALT_SIZE+AES.block_size]
    ciphertext_sans_salt = ciphertext[SALT_SIZE+AES.block_size:]
    key = generate_key_aes(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_CBC, IV)
    padded_plaintext = cipher.decrypt(ciphertext_sans_salt)
    plaintext = unpad_text(padded_plaintext)
    raw_file.write(plaintext)
    encrypted_file.close()
    raw_file.close()
    return True


def gen_hash_file(fname):
    file = open(fname)
    hash = hashlib.sha512()
    buffer_size = 4096
    while(file.read(buffer_size)):
        hash.update(file.read(buffer_size))
    file.close()
    file = open('./ftp_server/hash_files/hash_file.csv', 'ab')
    writer = csv.writer(file, delimiter='\t')
    row = []
    f = fname.strip().split('/')
    row.append(f[len(f)-1])
    row.append(hash.hexdigest())
    writer.writerow(row)
    file.close()
    return hash.hexdigest()


def genrate_keys_rsa():
        # RSA modulus length must be a multiple of 256 and >= 1024
    modulus_length = 256*8  # 2048 bit rsa key
    privatekey = RSA.generate(modulus_length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey.exportKey(), publickey.exportKey()


def rsa_encrypt(key, publickey):
    encrypted_key = publickey.encrypt(key, 32)[0]
    # base64 encoded strings are database friendly
    encoded_encrypted_key = base64.urlsafe_b64encode(encrypted_key)
    return encoded_encrypted_key


def rsa_decrypt(encoded_encrypted_key, privatekey):
    decoded_encrypted_key = base64.urlsafe_b64decode(encoded_encrypted_key)
    decoded_decrypted_key = privatekey.decrypt(decoded_encrypted_key)
    return decoded_decrypted_key