from user import *
from RSA_Auth import *

class BitCoin:
    def __init__(self):
        self.uni_users = {}

    def createUser(self, username):
        public_key, private_key = RSA_Auth.generateRSAKeys()
        user = User(username, public_key, private_key)
        self.uni_users[user.id] = user
        user.appInterface = self
        return user

    def notifyAllUsers(self, block):
        for userid in self.uni_users.keys():
            self._receiveBlock(userid, block)

    def _receiveBlock(self, userid, block):
        if (User.verify_signature(block.tranData, self.uni_users[block.tranData.payer_id].public_key)):
            self.uni_users[userid].blockChain.addBlock(block)

    def doTransaction(self, userA, userB, amount):
        userA.doTransaction(userB.id, amount)


if __name__ == "__main__":
    bitCoinApp = BitCoin()
    userA = bitCoinApp.createUser("userA")
    userB = bitCoinApp.createUser("userB")

    bitCoinApp.doTransaction(userA, userB, 10)
    bitCoinApp.doTransaction(userB, userA, 5)
    bitCoinApp.doTransaction(userA, userB, 20)

    for userid in bitCoinApp.uni_users:
        print(bitCoinApp.uni_users[userid].username)
        for block in bitCoinApp.uni_users[userid].blockChain.chainList:
            print("\t" + str(block))

