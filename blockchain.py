from hashlib import sha256
import json
import time
import logging

logging.basicConfig(filename="logs/log.log", encoding='utf-8', level=logging.DEBUG)

class Block:
    def __init__(self, index, transaction, timestamp, prev_hash, nonce=0):
        self.index = index
        self.transaction = transaction
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.nonce = nonce

    def make_hash(self):
        block_stringfy = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_stringfy.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.make_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    difficulty = 2
    def PoW(self, block):
        block.nonce = 0
        maked_hash = block.make_hash()
        while not maked_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            maked_hash = block.make_hash()
        return maked_hash

    ## CRUD

    def add_block(self, block, proof):
        prev_hash = self.last_block.hash
        #print(prev_hash)
        #print(block.prev_hash)
        if prev_hash != block.prev_hash:
            logging.critical("\nHASH DIFFERENCE LINE 50\n")
            return False
        if not self.validProof(block, proof):
            logging.critical("\nINVALID PoW LINE 53\n")
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def validProof(self, block, block_hash):
        logging.info(f"Validated PoW block {block.index}")
        return (block_hash.startswith('0' * Blockchain.difficulty) and (block_hash == block.make_hash()))

    def newTransaction(self, transaction):
        logging.info(f"New transaction --> {transaction}")
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            logging.critical("INCONSISTENT TRANSACTIONS LINE 67")
            return False

        for transaction in self.unconfirmed_transactions:
            last_block = self.last_block

            new_block = Block(index = last_block.index +1 , 
                                transaction = transaction,
                                timestamp = time.time(),
                                prev_hash = self.last_block.hash)
            proof = self.PoW(new_block)
            #print(proof)
            self.add_block(new_block, proof)
            #print(self.add_block(new_block, proof))
            self.unconfirmed_transactions = []
            
        return new_block.index
