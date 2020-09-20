from proof_of_work import *


class TransData:
    def __init__(self, payer_id, receiver_id, amount, signature=''):
        self.payer_id = payer_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.signature = signature

    def __eq__(self, other):
        if (self.payer_id == other.payer_id and \
                self.receiver_id == other.receiver_id and \
                self.amount == other.amount and \
                self.signature == other.signature):
            return True
        else:
            return False

    def __str__(self):
        return "" + \
               str(self.payer_id) + \
               " pay " + \
               str(self.amount) + \
               " to " + \
               str(self.receiver_id)

class Block:
    def __init__(self, tranData):
        self.prevHash = ''
        self.tranData = tranData
        self.hashIndex = 0
        self.hash = Mine.computeBlockHash(self)
        self.signature = ''

    def __str__(self):
        return "prevHash : {0}, transData : {1}, hash : {2}, hashIndex : {3}".format \
            (self.prevHash, self.tranData, self.hash, self.hashIndex)

    def __eq__(self, other):
        if self.prevHash == other.prevHash and \
                self.tranData == other.tranData and \
                self.hashIndex == other.hashIndex and \
                self.hash == other.hash and \
                self.signature == other.signature:
            return True
        else:
            return False

    def isLegal(self):
        print("block is legal:" + str(self.hash == Mine.computeBlockHash(self)))
        return self.hash == Mine.computeBlockHash(self)


class Chain:
    def __init__(self):
        self.chainList = []
        self.chainList.append(Block("genesis"))

    def addBlock(self, block):
        prevBlock = self.chainList[len(self.chainList) - 1]
        block.prevHash = prevBlock.hash
        block.hash, block.hashIndex = Mine.mine(block, diff_level=2)
        if self._verifyConsistency():
            self.chainList.append(block)


    def _verifyConsistency(self):
        if not self.chainList[0].isLegal():
            return False
        for item in range(1, len(self.chainList)):
            block = self.chainList[item]
            prevBlock = self.chainList[item - 1]
            if not (block.isLegal() and block.prevHash == prevBlock.hash):
                return False
        return True

if __name__ == "__main__":
    blockChain = Chain()
    firstBlock = Block(TransData("userA", "userB", 50 ))
    blockChain.addBlock(firstBlock)
    secondBlock = Block(TransData("userC", "userB", 20 ))
    blockChain.addBlock(secondBlock)
    thirdBlock = Block(TransData("userA", "userD", 40 ))
    blockChain.addBlock(thirdBlock)
    for block in blockChain.chainList:
        print(block)

    print(blockChain._verifyConsistency())
