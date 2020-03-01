set -a
. ./password
set +a

echo "Installing Hemerton Smart contract..."
sleep 5

cleos wallet open
cleos wallet unlock --password $PASSWORD
cleos wallet list
cleos wallet create_key >> key
sed -i 's/^[^"]*"//' key
sed -i 's/"//' key
sed -i 's/^/KEY=/' key

set -a
. ./key
set +a


cleos wallet import --private-key 5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3
cleos create account eosio hemerton $KEY -p eosio@active
cleos set contract hemerton /hemerton -p hemerton@active