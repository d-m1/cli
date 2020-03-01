# Hemerton CLI

> Version: **v0.0.1**

Hemerton's command line interface.

## Development environment

### Requisites

- Python 3.7+
- Virtualenv
- GNU Make
- Docker

### Setting up the project

```bash
# install blockchain & smart contract using docker
make setup-blockchain
# create a new virtualenv from Python 3.7
make setup-virtualenv
# activate the virtualenv
source .venv/bin/activate
# complete the cli setup
make setup-cli
```

# CLI Examples

```bash
- Requests Commands:
    # create a new request
    hemerton test new
    # upload corresponding evidence
    hemerton test upload
    # retrieve all requests
    hemerton test get

- Lists commands:
    # create a new list
    hemerton lists new
    # retrieve all lists
    hemerton lists get
```

### TODO:
Improve cli command names x)
