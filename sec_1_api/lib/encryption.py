from Crypto.Cipher import AES
import base64
import os


def encrypt_aes_base64(text, key):
    # the block size for the cipher object; must be 16 per FIPS-197
    block_size = 16

    padding = '{'
    pad = lambda s: s + (block_size - len(s) % block_size) * padding
    encode_aes = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    cipher = AES.new(key)
    encrypted = encode_aes(cipher, key)
    return base64.b64encode(encrypted).decode('utf-8')
