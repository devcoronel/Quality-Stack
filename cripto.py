from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

key = get_random_bytes(32)
iv = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC, iv)

def AES256CBC(data):
    data_bytes = bytes(data, 'utf-8')
    cifrado = cipher.encrypt(pad(data_bytes, 32))
    return cifrado

def key_para_cifrado():
    key_cifrado = str(key)
    return key_cifrado

def vi():
    iv_cifrado = str(iv)
    return iv_cifrado

def key_para_jwt():
    key_jwt = get_random_bytes(32)
    key_jwt = str(key_jwt)
    return key_jwt