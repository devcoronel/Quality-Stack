from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

import hashlib

key = b'\xc4Nu\xb8b\x95W\xe7=`\xde\x99\xfe"\xbb!\x07\xe8\x8fp\xfd8\xc2\x9a\xca\x89Qr\x14\xd1\xda\xaf'
iv = b'\xb7\xb3g\xb2\x07\x1e\xa9Y\xef;U\x7f\xf2a\xf4\xbf'
# key = get_random_bytes(32)
# iv = get_random_bytes(16)

def ENC_AES256CBC(data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data_bytes = bytes(data, 'utf-8')
    cifrado = cipher.encrypt(pad(data_bytes, 32))
    # result = [cifrado, key, iv]
    return cifrado

def DEC_AES256CBC(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data_descifrado = unpad(cipher.decrypt(data), 32)
    descifrado = data_descifrado.decode('utf-8')
    return descifrado

def key_para_jwt():
    key_jwt = get_random_bytes(32)
    key_jwt = str(key_jwt)
    return key_jwt

def SHA256(data):
    # La data será un string
    data = data.encode('utf-8')
    data = hashlib.sha256(data)
    data = data.digest()
    # El hasheo retorna bytes
    return data

