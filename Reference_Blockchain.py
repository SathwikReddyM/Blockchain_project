# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 12:21:34 2022

@author: Sathwik Reddy M
"""

import datetime
import hashlib
import json
from flask import Flask, jsonify

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, prev_hash='0')
        
    def create_block(self, proof, prev_hash):
        block = {"block_number" : len(self.chain)+1,
                 "timestamp" : str(datetime.datetime.now()),
                 "proof" : proof,
                 "prev_hash" : prev_hash
                 }
        self.chain.append(block)
        return block
    
    def get_prev_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        state = False
        while state != True:
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                state = True
            else:
                new_proof += 1
        return new_proof
            
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

                
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
#part-2 - mining
# creating a web app
app = Flask(__name__)
    
#creating a blockchain
blockchain = Blockchain()

#Mining now
@app.route('/mine_block', methods = ['GET'] )
def mine_block():
    previous_block = blockchain.get_prev_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    prev_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, prev_hash)
    response = {'message' : 'You just mined a Block',
                'index': block['block_number'],
                'timestamp': block['timestamp'],
                'proof' : block['proof'],
                'prev_hash' : block['prev_hash']
                }
    return jsonify(response) , 200
    

# Getting full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200





@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message':'Yes its valid'}
    else:
        response = {'message': 'No its not valid'}
    return jsonify(response), 200

#Running the app
app.run(host = '0.0.0.0', port = 5000)



    
    
    
    
    
            
            
            
            
            
            
            