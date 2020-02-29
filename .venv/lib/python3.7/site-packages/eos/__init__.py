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

