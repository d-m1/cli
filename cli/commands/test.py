from copy import deepcopy
from typing import Tuple, Iterable
import click
import ast
from eos import eos_client, eos_key, ADMIN, open_req, show_transaction_response, upload_req

from .terminal import prompt, OptionList, Input, validate_string, validate_integer


@click.group()
def test() -> None:
    """Test commands.
    """
    pass


def _get_request_form(lists: Iterable[str]) -> Tuple[OptionList, ...]:
    """Retrieves input data from user in order to send a new request."""
    return (
        OptionList(
            "numlist",
            message="Selecciona una lista para la petición: ",
            choices=lists,
        ), )


def _get_upload_form() -> Tuple[Input, ...]:
    return (
        Input(
            "request",
            message="ID de la request: ",
            default="1",
            validate=validate_integer(
                min_int=1, max_int=65536, optional=False
            ),
        ),
        Input(
            "evidence",
            message="Evidencia (hash del video) en formato string hexadecimal: ",
            default="27362e4afa18a31c6bf",
            validate=validate_string(max_char=100, optional=False),
        ),
    )


def _get_last_request_data() -> int:
    """Retrieves the information about the last request."""
    table = eos_client.get_table('hemerton', 'hemerton', 'proofs', limit=99999)['rows']
    result = table.pop()
    return result['key'], result['actions']


@test.command()
def new() -> None:
    """Sends a new request to the Smart Contract"""
    # Retrieve existing lists
    lists = eos_client.get_table('hemerton', 'hemerton', 'lists', limit=99999)['rows']
    if not lists:
        print('At least a list is meant to be registered before send a request.')
        print('Try using the following command: hemerton lists new.')
        print('Exiting...')
        return
    lists_prompt = [str(row['numlist']) for row in lists]
    # Request user data
    arguments = prompt(_get_request_form(lists_prompt))
    # Cast strings to corresponding types
    arguments = {k: ast.literal_eval(v) for k, v in arguments.items()}
    # Add admin user to request
    arguments['user'] = ADMIN

    payload = deepcopy(open_req)
    # Converting payload to binary
    data = eos_client.abi_json_to_bin(payload['account'], payload['name'], arguments)
    # Inserting payload binary form as "data" field in original payload
    payload['data'] = data['binargs']
    # final transaction formed
    trx = {"actions": [payload]}
    resp = eos_client.push_transaction(trx, eos_key, broadcast=True)
    print("Processing TX...")
    request_id, vector = _get_last_request_data()
    x_ax = len(vector) / 4
    matrix = [vector[x:x+x_ax] for x in xrange(0, len(vector), x_ax)]
    print('------------------------------------------------')
    print(f"Your request ID is {str(request_id)}")
    print("Keep it safe in order to use it when you upload the evidence.")
    print('------------------------------------------------')
    print("MIT Matrix (Actions): ")
    for row in matrix:
        print(f"{row}")
    show_transaction_response(resp)


@test.command()
def upload() -> None:
    """Uploads an evidence to an existing request"""
    # Request user data
    arguments = prompt(_get_upload_form())
    # Cast strings to corresponding types
    arguments = {k: (ast.literal_eval(v) if k == 'request' else v)
                 for k, v in arguments.items()
                 }
    # Add admin user to request
    arguments['user'] = ADMIN

    payload = deepcopy(upload_req)
    # Converting payload to binary
    data = eos_client.abi_json_to_bin(payload['account'], payload['name'], arguments)
    # Inserting payload binary form as "data" field in original payload
    payload['data'] = data['binargs']
    # final transaction formed
    trx = {"actions": [payload]}
    resp = eos_client.push_transaction(trx, eos_key, broadcast=True)
    print("Processing TX...")
    print('------------------------------------------------')
    print(f"Final state of the register in EOS Blockchain:")
    table = eos_client.get_table('hemerton', 'hemerton', 'proofs', limit=99999)['rows']
    for row in table:
        if row['key'] == arguments['request']:
            print(row)
            break
    show_transaction_response(resp)


@test.command()
def get() -> None:
    """Retrieves all the requests from the Smart Contract"""
    print(f"Showing existing requests:")
    table = eos_client.get_table('hemerton', 'hemerton', 'proofs', limit=99999)
    for row in table['rows']:
        print(f"{row}")
