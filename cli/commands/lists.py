from copy import deepcopy
from typing import Optional, Tuple
import click
import ast
from eos import eos_client, eos_key, ADMIN, newlist, show_transaction_response

from .terminal import validate_integer, validate_string, Input, prompt


@click.group()
def lists() -> None:
    """Lists commands.
    """
    pass


def _get_list_form(optional: Optional[bool] = False) -> Tuple[Input, ...]:
    """Retrieves input data from user in order to set or config a new list.

        Args:
            optional: Flag to set mandatory fields.
    """

    return (
        Input(
            "numlist",
            message="Numero de lista (ID): ",
            default="1",
            validate=validate_integer(
                min_int=1, max_int=65536, optional=optional
            ),
        ),
        Input(
            "nAccMax",
            message="nAccMax: ",
            default="9",
            validate=validate_integer(
                min_int=1, max_int=65536, optional=optional
            ),
        ),
        Input(
            "durMaxAcc",
            message="durMaxAcc: ",
            default="5",
            validate=validate_integer(
                min_int=1, max_int=65536, optional=optional
            ),
        ),
        Input(
            "durPru",
            message="durPru: ",
            default="60",
            validate=validate_integer(
                min_int=1, max_int=65536, optional=optional
            ),
        ),
        Input(
            "sRes",
            message="sRes: ",
            default="0",
            validate=validate_integer(
                min_int=0, max_int=65536, optional=optional
            ),
        ),
        Input(
            "nTAT",
            message="nTaT (Int array []): ",
            default="[30,60]",
            validate=validate_string(max_char=50, optional=optional),
        ),
        Input(
            "nAT",
            message="nAT: ",
            default="50",
            validate=validate_integer(
                min_int=1, max_int=65536, optional=optional
            ),
        ),
        Input(
            "vNAccR",
            message="vNAccR (Int array []): ",
            default="[2,2]",
            validate=validate_string(max_char=50, optional=optional),
        ),
        Input(
            "vNR",
            message="vNR (Int array []): ",
            default="[2,2]",
            validate=validate_string(max_char=50, optional=optional),
        ),
        Input(
            "action_p_action_p_restriction",
            message="Tipos de acciones por accion por cada restriccion (Int array []): ",
            default="[1,2,2,2]",
            validate=validate_string(max_char=50, optional=optional),
        ),
        Input(
            "x_axis",
            message="Eje x de la matriz anterior: ",
            default="2",
            validate=validate_integer(
                min_int=1, max_int=30, optional=optional
            ),
        ),
        Input(
            "y_axis",
            message="Eje y de la matriz anterior: ",
            default="2",
            validate=validate_integer(
                min_int=1, max_int=30, optional=optional
            ),
        )
    )


@lists.command()
def new() -> None:
    """Sends a new actions list to the Smart Contract"""
    # Request user data
    arguments = prompt(_get_list_form())
    # Cast strings to corresponding types
    arguments = {k: ast.literal_eval(v) for k, v in arguments.items()}
    # Add admin user to request
    arguments['user'] = ADMIN

    payload = deepcopy(newlist)
    # Converting payload to binary
    data = eos_client.abi_json_to_bin(payload['account'], payload['name'], arguments)
    # Inserting payload binary form as "data" field in original payload
    payload['data'] = data['binargs']
    # final transaction formed
    trx = {"actions": [payload]}
    resp = eos_client.push_transaction(trx, eos_key, broadcast=True)
    print('------------------------------------------------')
    print(f"New list {arguments['numlist']} registered successfully")
    show_transaction_response(resp)


@lists.command()
def get() -> None:
    """Retrieves all the action lists from the Smart Contract"""
    print(f"Showing existing lists:")
    table = eos_client.get_table('hemerton', 'hemerton', 'lists', limit=5000)
    for row in table['rows']:
        print(f"{row}")
