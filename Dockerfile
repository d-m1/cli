FROM ubuntu:18.04

RUN apt update && apt upgrade -y
RUN apt install -y wget curl 

RUN wget https://github.com/EOSIO/eos/releases/download/v1.8.6/eosio_1.8.6-1-ubuntu-18.04_amd64.deb
RUN apt install -y ./eosio_1.8.6-1-ubuntu-18.04_amd64.deb

RUN wget https://github.com/EOSIO/eosio.cdt/releases/download/v1.6.3/eosio.cdt_1.6.3-1-ubuntu-18.04_amd64.deb
RUN apt install -y ./eosio.cdt_1.6.3-1-ubuntu-18.04_amd64.deb

RUN mkdir hemerton
COPY hemerton.wasm /hemerton/
COPY hemerton.abi /hemerton/
COPY install.sh .

RUN keosd &
RUN cleos wallet create -f password
RUN sed -i 's/^/PASSWORD=/' password

CMD nodeos -e -p eosio -d --plugin eosio::producer_plugin --plugin eosio::chain_api_plugin --plugin eosio::http_plugin --plugin eosio::history_plugin --plugin eosio::history_api_plugin --http-server-address=0.0.0.0:8888 --filter-on="*" --access-control-allow-origin='*' --contracts-console --http-validate-host=false --verbose-http-errors