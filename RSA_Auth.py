from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64

class RSA_Auth:
    @staticmethod
    def getKeyFromFile(keyfile):
        with open(keyfile, 'r') as f:
            key = f.read()
            return key


    @staticmethod
    def encrypt(data, public_key):
        rsakey = RSA.importKey(public_key)
        cipher = Cipher_PKCS1_v1_5.new(rsakey)
        return base64.b64encode(cipher.encrypt(data.encode('utf-8')))

    @staticmethod
    def decrypt(cipher_text, private_key):
        rsakey = RSA.importKey(private_key)
        cipher = Cipher_PKCS1_v1_5.new(rsakey)
        return cipher.decrypt(base64.b64decode(cipher_text), Random.new().read)

    @staticmethod
    def sign(data, private_key):
        rsakey = RSA.importKey(private_key)
        signer = Signature_PKCS1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(data.encode('utf-8'))
        signature = signer.sign(digest)
        return base64.b64encode(signature)

    @staticmethod
    def verify_signature(signature, data, public_key):
        rsakey = RSA.importKey(public_key)
        verifier = Signature_PKCS1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(data.encode('utf-8'))
        return verifier.verify(digest, base64.b64decode(signature))

    @staticmethod
    def generateRSAKeys(keyLen = 1024):
        rsa = RSA.generate(keyLen, Random.new().read)
        private_key = rsa.exportKey()
        public_key = rsa.publickey().exportKey()
        return (public_key, private_key)

if __name__ == "__main__":
    public_key = "id_rsa.pub"
    private_key = "id_rsa"
    data = "hello 1"
    cipher_text = RSA_Auth.encrypt("hello", RSA_Auth.getKeyFromFile(public_key))
    print(RSA_Auth.decrypt(cipher_text, RSA_Auth.getKeyFromFile(private_key)))

    signature = RSA_Auth.sign(data, RSA_Auth.getKeyFromFile(private_key))
    print(RSA_Auth.verify_signature(signature, data, RSA_Auth.getKeyFromFile(public_key)))