from web3 import Web3


def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/423cb917c76d4eb5a9634424ca71ac81'))
    address = '0x2c5171518B41D5f2015337a219F307F3bC19D108'
    privateKey = '0xf638b2528aa8a808f7a614465ea1c2c7ec35bee087168e2a260e230b3877d7f7'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas=10000000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')), privateKey)

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId

