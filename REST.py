from flask import Flask, request
import requests
import json

import blockchain

blockchain = blockchain.Blockchain()

app =  Flask(__name__)

@app.route("/chain", methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"lenght": len(chain_data), "chain":chain_data})

@app.route("/addTrans", methods=['GET', 'POST'])
def add_trans():
    trans_data = []
    if request.method == 'POST':
        data = request.form["data"]

    blockchain.newTransaction(data)
    
    return data

@app.route("/mine", methods=['GET'])
def mine():
    return str(blockchain.mine())

@app.route("/transList", methods=['GET'])
def transList():
    print(blockchain.unconfirmed_transactions)
    return str(blockchain.unconfirmed_transactions)

@app.route("/indexs", methods=['GET'])
def indexs():
    return str(blockchain.last_block.index)

    
    

app.run(debug=True, port=5000)
