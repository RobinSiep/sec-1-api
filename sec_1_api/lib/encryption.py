from Crypto.PublicKey import RSA
import base64


def rsa_encrypt_base64(key, text):
    # generate pub key for prototype purpose
    key = RSA.generate(2048)
    gen_pub_key = key.publickey().exportKey('DER')

    pub_key = RSA.importKey(gen_pub_key)
    encrypted = pub_key.encrypt(text.encode('utf-8'), '32')[0]
    return base64.b64encode(encrypted).decode('utf-8')
