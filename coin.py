import hashlib
from collections import OrderedDict
from datetime import datetime

class Coin():

    def __init__(self, symbol, supply, wallets):
        self.coin_symbol = symbol
        self.total_supply = supply
        self.wallets = wallets
        self.wallets["owner"] = supply
        self.txns = []
        self.past_transaction = OrderedDict()


    def blockchains_info(self):
        info = {
            "coin_symbol": self.coin_symbol,
            "total_supply": str(self.total_supply),
            "num_txns": str(len(self.txns))
        }
        if len(self.txns) > 0: info["merkle_root"] = self.txns[-1]["merkle_root"]
        
        for k, v in self.wallets.items():
            info["wallet_id_{}".format(k)] = str(v)
        
        for index in range(0, len(self.txns)):
            info["txn_id_{}".format(index)] = str(self.txns[index])
        
        return info
       
 
    def get_timestamp(self):
        return str(datetime.now())


    def transfer(self, from_wallet, to_wallet, amount):
        # If one of the below pre-conditions fails, return False
        # check if the from_wallet is valid
        # check if the to_wallet is valid
        # check the from_wallet has sufficient amount
         # Move value amount from "from_wallet" to "to_wallet"
     

        wallet_keys=list(self.wallets)
        print(wallet_keys)
        if(from_wallet not in wallet_keys ):
            return False
        if(to_wallet not in wallet_keys ):
            return False
        from_value= self.wallets[from_wallet]
        to_value= self.wallets[to_wallet]
        if(from_value<amount):
            return False

        
        to_value=to_value+amount
        from_value=from_value - amount



       

        return True


    def dict_to_string(self, dict):
        return ''.join(''.join((k, str(v))) for k,v in dict.items()).encode('utf-8')

    def add_txn_to_blockchain(self, from_wallet, to_wallet, amount):
        txn = { 
            "from_wallet": from_wallet, 
            "to_wallet": to_wallet,
            "amount": amount,
            "time_stamp": self.get_timestamp()
        }
        current_hash = hashlib.sha256(self.dict_to_string(txn)).hexdigest()
        txn["hash"] = current_hash
        working_txns = list(self.txns)
        working_txns.append(txn)
        is_odd = (len(working_txns) % 2) != 0
        if is_odd: working_txns.append(txn)
        
        working_hashes = []
        for working_txn in working_txns:
            working_hashes.append(working_txn["hash"])
        new_merkle_root = self.compute_merkle_root(working_hashes)
        txn["merkle_root"] = new_merkle_root
        self.txns.append(txn)


    def compute_merkle_root(self, children):
        """
        Generating a Merkle root hash using the given list of transactions. You need to recursively build up 
        a (binary) tree to get to the root and then return the root.
        @see - http://orm-chimera-prod.s3.amazonaws.com/1234000001802/images/msbt_0702.png
        The calling code add_txn_to_blockchain() guarantees that the children list contains even number of transaction hash only.
        
        Example: hashlib.sha256( (x).encode('utf-8') ).hexdigest()

        :params children: a list of transaction hash in order. ['xxxxxx', 'yyyyyy', 'zzzzzz', 'aaaaaaa']
        :return a Merkle root hash
        """
 
     


        listoftransaction = children
        past_transaction = self.past_transaction
        temp_transaction = []
        for index in range(0,len(listoftransaction),2):
            current = listoftransaction[index]
            if index+1 != len(listoftransaction):
                current_right = listoftransaction[index+1]
            else:
                current_right = ''
            current_hash = hashlib.sha256(current.encode('utf-8'))
            
            if current_right != '':
                current_right_hash = hashlib.sha256(current_right.encode('utf-8'))
            
            past_transaction[listoftransaction[index]] = current_hash.hexdigest()
            
            if current_right != '':
                past_transaction[listoftransaction[index+1]] = current_right_hash.hexdigest()
            
            if current_right != '':
                temp_transaction.append(current_hash.hexdigest() + current_right_hash.hexdigest())
                
            else:
                temp_transaction.append(current_hash.hexdigest())
                
        if len(listoftransaction) != 1:
            children = temp_transaction
            self.past_transaction = past_transaction
            self.compute_merkle_root(children)
        

        else:
            last_key = list(self.past_transaction.keys())[-1]
            return self.past_transaction[last_key]

         

    
    def debug_print(self):
        print("coin_symbol: {}".format(self.coin_symbol))
        print("total_supply: {}".format(self.total_supply))
        print("num_txns: {}".format(len(self.txns)))
        if len(self.txns) > 0: print("merkle_root: {}".format(self.txns[-1]["merkle_root"]))
        
        print("---- WALLET START ----")
        for k, v in self.wallets.items():
            print("wallet_id:{}, wallet_balance:{}".format(k, v))
        print("---- WALLET END ----")

        print("---- TXN START ----")
        for txn in self.txns:
            print(txn)
        print("---- TXN END ----")


# Test code to test this Coin class independently
if __name__ == '__main__':
    coin = Coin('CMPE_Coin', 100, { "Alice": 0, "Bob": 0 })
    if coin.transfer("owner", "Alice", 10): 
        coin.add_txn_to_blockchain("owner", "Alice", 10)
    if coin.transfer("Alice", "Bob", 5): 
        coin.add_txn_to_blockchain("Alice", "Bob", 5)
    coin.debug_print()
    
