# standard library
import pprint
import re
from copy import deepcopy
from typing import Any, Callable, Dict, Iterable, Optional, Union

# third party packages
from PyInquirer import Separator, Token
from PyInquirer import prompt as pyinquirer_prompt
from PyInquirer import style_from_dict
from termcolor import cprint
from typing_extensions import Literal

pp = pprint.PrettyPrinter(indent=4)

_THEME = style_from_dict(
    {
        Token.QuestionMark: "bold",
        Token.Selected: "#673AB7 bold",
        Token.Instruction: "",  # default
        Token.Answer: "#3ba09d",
        Token.Question: "bold",
    }
)

_PROMPT_ICON = "-"


def _assign_from_q(
    target_dict: Dict[str, Any],
    key: str,
    q: "_Question",
    attr: Optional[str] = None,
    default: Any = None,
) -> None:
    attr = attr or key
    value = getattr(q, attr, None) or default
    if value is not None:
        target_dict[key] = value


def _unpack_questions(questions: Iterable["_Question"]) -> Any:
    unpacked = []
    for q in questions:
        if not isinstance(q, _Question):
            raise TypeError("Not a valid question class")

        unpacked_q = {"name": q.name, "qmark": _PROMPT_ICON}

        if isinstance(q, Input):
            unpacked_q["type"] = "input"
            _assign_from_q(
                unpacked_q, "message", q, default=f"{q.name.capitalize()}:"
            )
            _assign_from_q(unpacked_q, "default", q)
            _assign_from_q(unpacked_q, "validate", q)
            _assign_from_q(unpacked_q, "filter", q)

        if isinstance(q, OptionList) or isinstance(q, RawList):
            if isinstance(q, OptionList):
                unpacked_q["type"] = "list"
            if isinstance(q, RawList):
                unpacked_q["type"] = "rawlist"
            _assign_from_q(
                unpacked_q, "message", q, default=f"{q.name.capitalize()}:"
            )
            _assign_from_q(unpacked_q, "default", q)
            _assign_from_q(unpacked_q, "choices", q)
            _assign_from_q(unpacked_q, "filter", q)
            _assign_from_q(unpacked_q, "separator", q)

        if isinstance(q, CheckBox):
            unpacked_q["type"] = "checkbox"
            _assign_from_q(
                unpacked_q, "message", q, default=f"{q.name.capitalize()}:"
            )
            _assign_from_q(unpacked_q, "default", q)
            _assign_from_q(unpacked_q, "choices", q)
            _assign_from_q(unpacked_q, "filter", q)
            _assign_from_q(unpacked_q, "validate", q)

        unpacked.append(unpacked_q)

    return unpacked


class _Question:
    name: str


# public
# ------


class Input(_Question):
    def __init__(
        self,
        name: str,
        *,
        message: Optional[Union[str, Dict[str, Any]]] = None,
        default: Optional[
            Union[str, int, Iterable[Any], Callable[[Dict[str, Any]], Any]]
        ] = None,
        validate: Optional[Callable[[str], Union[bool, str]]] = None,
        input_filter: Optional[Callable[[str], Any]] = None,
    ):
        self.name = name
        self.message = message
        self.default = default
        self.validate = validate
        self.filter = input_filter


class OptionList(_Question):
    def __init__(
        self,
        name: str,
        *,
        message: Optional[Union[str, Dict[str, Any]]] = None,
        default: Optional[
            Union[str, int, Iterable[Any], Callable[[Dict[str, Any]], Any]]
        ] = None,
        choices: Optional[
            Union[
                str,
                int,
                Separator,
                Iterable[Any],
                Callable[[Dict[str, Any]], Any],
            ]
        ] = None,
        input_filter: Optional[Callable[[str], Any]] = None,
    ):
        self.name = name
        self.message = message
        self.default = default
        self.choices = choices
        self.filter = input_filter


class RawList(OptionList):
    pass


class CheckBox(_Question):
    def __init__(
        self,
        name: str,
        *,
        message: Optional[Union[str, Dict[str, Any]]] = None,
        default: Optional[
            Union[str, int, Iterable[Any], Callable[[Dict[str, Any]], Any]]
        ] = None,
        choices: Optional[
            Union[
                str,
                int,
                Separator,
                Iterable[Any],
                Callable[[Dict[str, Any]], Any],
            ]
        ] = None,
        validate: Optional[Callable[[str], Union[bool, str]]] = None,
        input_filter: Optional[Callable[[str], Any]] = None,
    ):
        self.name = name
        self.message = message
        self.default = default
        self.choices = choices
        self.validate = validate
        self.filter = input_filter


def prompt(
    questions: Iterable[_Question], remove_empty: bool = True
) -> Dict[str, Any]:
    prompt_style = _THEME
    unpacked_questions = _unpack_questions(questions)
    answers = pyinquirer_prompt(unpacked_questions, style=prompt_style)
    final_answers: Dict[str, Any] = deepcopy(answers)

    if remove_empty:
        for key, value in answers.items():
            if isinstance(value, str):
                if not value:
                    del final_answers[key]

    return final_answers


def log_error(msg: str) -> None:
    cprint(
        f"ERROR: {msg}", color="red", attrs=["bold"],
    )


def log_message(msg: str) -> None:
    cprint(
        f"{msg}", attrs=["bold"],
    )


def validate_string(
    min_char: Optional[int] = None,
    max_char: Optional[int] = None,
    regexp: Optional[str] = None,
    regexp_message: Optional[str] = None,
    optional: Optional[bool] = False,
) -> Callable[[str], Union[Literal[True], str]]:
    length_error_msg = (
        "Length must be between "
        f"{min_char if min_char is not None else 'infinite'} "
        f"and {max_char if max_char is not None else 'infinite'}"
    )

    def fn(val: str) -> Union[Literal[True], str]:
        if not val:
            if optional:
                return True
            else:
                return "Parameter is required"

        if (min_char is not None and len(val) < min_char) or (
            max_char is not None and len(val) > max_char
        ):
            return length_error_msg

        if regexp and re.match(regexp, val) is None:
            return (
                regexp_message
                or "Incorrect format (regular expression does not match)"
            )

        return True

    return fn


def validate_integer(
    min_int: Optional[int] = None,
    max_int: Optional[int] = None,
    optional: Optional[bool] = False,
) -> Callable[[str], Union[Literal[True], str]]:
    type_error_msg = "Value must be a number"
    range_error_msg = (
        "Value must be between "
        f"{min_int if min_int is not None else 'infinite'} "
        f"and {max_int if max_int is not None else 'infinite'}"
    )

    def fn(val: str) -> Union[Literal[True], str]:
        if not val:
            if optional:
                return True
            else:
                return "Parameter is required"
        try:
            val_int = int(val)
        except ValueError:
            return type_error_msg

        if (max_int is not None and val_int > max_int) or (
            min_int is not None and val_int < min_int
        ):
            return range_error_msg

        return True

    return fn


def validate_float(
    min_float: Optional[float] = None,
    max_float: Optional[float] = None,
    optional: Optional[bool] = False,
) -> Callable[[str], Union[Literal[True], str]]:
    type_error_msg = "Value must be a floating point number"
    range_error_msg = (
        "Value must be between "
        f"{min_float if min_float is not None else 'infinite'} "
        f"and {max_float if max_float is not None else 'infinite'}"
    )

    def fn(val: str) -> Union[Literal[True], str]:
        if not val:
            if optional:
                return True
            else:
                return "Parameter is required"
        try:
            val_float = float(val)
        except ValueError:
            return type_error_msg

        if (max_float is not None and val_float > max_float) or (
            min_float is not None and val_float < min_float
        ):
            return range_error_msg

        return True

    return fn
