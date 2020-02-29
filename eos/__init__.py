from typing import Dict

from eospy.cleos import Cleos
import eospy.keys

ADMIN = 'eosio'

eos_client = Cleos()
eos_key = eospy.keys.EOSKey('5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3')

newlist = {
        "account": "hemerton",
        "name": "newlist",
        "authorization": [{
            "actor": "eosio",
            "permission": "owner",
        }],
    }

open_req = {
        "account": "hemerton",
        "name": "open",
        "authorization": [{
            "actor": "eosio",
            "permission": "owner",
        }],
    }


upload_req = {
        "account": "hemerton",
        "name": "upload",
        "authorization": [{
            "actor": "eosio",
            "permission": "owner",
        }],
    }


def show_transaction_response(resp: Dict) -> None:
    print('------------------------------------------------')
    print('------------------------------------------------')
    print(f"TX: {resp['transaction_id']} executed successfully")
    print(f"Block num: {resp['processed']['block_num']}")
    print(f"Block time: {resp['processed']['block_time']}")
    print(f"Receiver (SMC): {resp['processed']['action_traces'][0]['receipt']['receiver']}")
    print('------------------------------------------------')
