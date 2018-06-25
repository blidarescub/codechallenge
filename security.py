import base64

from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


SALT = "c0d3ch@ll3ng3"


def generate_keys():
    modulus_length = 2048  # must be a multiple of 256 and >= 1024
    privatekey = RSA.generate(modulus_length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey, publickey


def encrypt_w(word, publickey):
    cipher = PKCS1_OAEP.new(publickey)
    encrypted_word = cipher.encrypt(word.encode('utf-8'))
    encoded_encrypted_word = base64.b64encode(encrypted_word)
    return encoded_encrypted_word


def decrypt_w(encoded_word, privatekey):
    cipher = PKCS1_OAEP.new(privatekey)
    decoded_encrypted_word = base64.b64decode(encoded_word)
    decoded_decrypted_word = cipher.decrypt(decoded_encrypted_word)
    return decoded_decrypted_word.decode('utf-8')


def export_key(key, private=False):
    keyname = 'private_key.pem' if private else 'public_key.pem'
    f = open(keyname, 'wb')
    f.write(key.exportKey('PEM'))
    f.close()


def import_key(keyfile):
    f = open(keyfile, 'r')
    newkey = RSA.importKey(f.read())
    f.close()
    return newkey
