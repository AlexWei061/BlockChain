import hashlib

class Mine:
    @staticmethod
    def _blockSeed(block):
        seed = block.prevHash + str(block.tranData) + str(block.hashIndex)
        return seed

    @staticmethod
    def computeBlockHash(block):
        return hashlib.sha256(Mine._blockSeed(block).encode('utf-8')).hexdigest()

    @staticmethod
    def computeHash(data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def _proofOfWork(data, diff_level):
        prefix = ''.join(['0' for _ in range(diff_level)])
        # print(prefix)

        index = 0
        while True:
            index += 1
            seed = data + str(index)
            hashkey = Mine.computeHash(seed)
            if (hashkey[0:diff_level] == prefix):
                return (hashkey, index)

    @staticmethod
    def _mine(data, diff_level = 9):
        return Mine._proofOfWork(data, diff_level)

    @staticmethod
    def mine(block, diff_level = 9):
        return Mine._mine(block.prevHash+str(block.tranData), diff_level)