#!/usr/bin/env python3
"""AES-CBC encryption and decryption for account info."""

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64 as b64
import random
import json
import os.path

FILE_NAME = "aes_account.json"
AES_ACCOUNT_KEY = "aes_account_key"
XOR_KEY = "xor_key"
KEY_KEY = "key_key"


class AesCBC:

    # random_16
    def random_16(self):
        str = ""
        return str.join(
            random.choice("abcdefghijklmnopqrstuvwxyz!@#$%^&*1234567890")
            for i in range(16)
        )

    # add_to_16
    def add_to_16(self, text):
        if len(text.encode("utf-8")) % 16:
            add = 16 - (len(text.encode("utf-8")) % 16)
        else:
            add = 0
        text = text + ("\0" * add)
        return text.encode("utf-8")

    # cbc_encryption
    def cbc_encrypt(self, key, iv, text):
        key = key.encode("utf-8")
        mode = AES.MODE_CBC
        iv = bytes(iv, encoding="utf8")
        text = self.add_to_16(text)
        cryptos = AES.new(key, mode, iv)
        cipher_text = cryptos.encrypt(text)
        return str(b2a_hex(cipher_text), encoding="utf-8")

    # cbc_decryption
    def cbc_decrypt(self, key, iv, text):
        key = key.encode("utf-8")
        iv = bytes(iv, encoding="utf8")
        mode = AES.MODE_CBC
        cryptos = AES.new(key, mode, iv)
        plain_text = cryptos.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip("\0")

    # xor_encrypt
    def xor_encrypt(self, data, key):
        lkey = len(key)
        secret = []
        num = 0
        for each in data:
            if num >= lkey:
                num = num % lkey
            secret.append(chr(ord(each) ^ ord(key[num])))
            num += 1
        return b64.b64encode("".join(secret).encode()).decode()

    # xor_decrypt
    def xor_decrypt(self, secret, key):
        tips = b64.b64decode(secret.encode()).decode()
        lkey = len(key)
        secret = []
        num = 0
        for each in tips:
            if num >= lkey:
                num = num % lkey
            secret.append(chr(ord(each) ^ ord(key[num])))
            num += 1
        return "".join(secret)

    # add xor to cache
    def add_xor_cache(self, xor, key):
        xor_info = {}
        xor_info[XOR_KEY] = xor
        xor_info[KEY_KEY] = key
        with open(FILE_NAME, "w") as file_obj_w:
            json.dump(xor_info, file_obj_w)

    # whether xor cache exist
    def exist_xor_cache(self):
        return os.path.isfile(FILE_NAME)

    # get xor from cache
    def get_xor_cache(self):
        with open(FILE_NAME) as file_obj_r:
            xor_info = json.load(file_obj_r)
        return xor_info

    # json to dict
    def json_to_dict(self, json_str):
        return json.loads(json_str)

    # confuse str
    def b64_encrypt(self, text):
        return b64.b64encode(text.encode()).decode()

    # unconfuse str
    def b64_decrypt(self, text):
        return b64.b64decode(text).decode()
