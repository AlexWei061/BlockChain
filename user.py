import uuid
from RSA_Auth import *
from block_chain import *

class User:
    def __init__(self, username, public_key, private_key):
        self.username = username
        self.id = uuid.uuid4()
        self.public_key = public_key
        self.private_key = private_key
        self.blockChain = Chain()
        self.appInterface = None

    def sign(self, trans_data):
        trans_data.signature = RSA_Auth.sign(str(trans_data), self.private_key)

    @staticmethod
    def verify_signature(trans_data, user_pub_key):
        return RSA_Auth.verify_signature(trans_data.signature, str(trans_data), user_pub_key)

    def doTransaction(self, receiver_id, amount):
        trans_data = TransData(self.id, receiver_id, amount)
        self.sign(trans_data)
        block = Block(trans_data)
        self._broadcastBlock(block)

    def _broadcastBlock(self, block):
        if self.appInterface != None:
            self.appInterface.notifyAllUsers(block)


if __name__ == "__main__":
    userA_pub_key = RSA_Auth.getKeyFromFile("id_rsa_A.pub")
    userA_priv_key = RSA_Auth.getKeyFromFile("id_rsa_A")
    userA = User("userA",userA_pub_key, userA_priv_key)
    userB_pub_key = RSA_Auth.getKeyFromFile("id_rsa_B.pub")
    userB_priv_key = RSA_Auth.getKeyFromFile("id_rsa_B")
    userB = User("userB",userB_pub_key, userB_priv_key)

    userA.doTransaction(userB.id, 10)
    userB.doTransaction(userA.id, 5)
