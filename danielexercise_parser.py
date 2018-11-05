# Utilities for prompting the user for data

from typing import List, Callable, TypeVar


T = TypeVar("T")


def generate_parser(obj_desc: str, parser: Callable[[str], T]) -> Callable[[str], T]:
    """
    generate_parser(obj_desc: str, parser: Callable[[str], T]) -> parse_func: Callable[[str], T]

    Returns a parsing that takes a prompt string and uses this function's argument error string and parser.
    """
    error = "Please try again with a valid " + obj_desc
    def result(prompt: str) -> T:
        """
        result(prompt: str) -> result: T

        Prompts the command line for an value and returns it.
        If the input is not valid, this function keeps on trying again.
        """
        while True:
            try:
                return parser(input(prompt))
            except ValueError:
                print(error)
    return result


parse_int = generate_parser("integer", int)
parse_int.__doc__ = """
    parse_int(prompt: str) -> result: int

    Prompts the command line for an integer and returns it.
    If the input is not a valid integer, this function keeps on trying again.
    """


parse_float = generate_parser("decimal", int)
parse_float.__doc__ = """
    parse_float(prompt: float) -> result: float

    Prompts the command line for a floating-point number and returns it.
    If the input is not a valid floating-point number, this function keeps on trying again.
    """


def generate_list_parser(obj_desc: str, parser: Callable[[str], T]) -> Callable[[str], List[T]]:
    """
    generate_list_parser(obj_desc: str, parser: Callable[[str], T]) -> parse_func: Callable[[str], List[T]]

    Returns a parsing function that takes a prompt string and uses this function's argument error string and parser.
    """
    error = "Please try again with a valid comma-separated " + obj_desc + " list"
    def result(prompt: str) -> List[T]:
        """
        result(prompt: str) -> result: List[T]; len(result) > 0

        Prompts the command line for a list of values and returns it.
        If the input is not valid, this function keeps on trying again.
        """
        while True:
            try:
                input_str = input(prompt)
                split = input_str.split(",")
                result_ = []
                for part in split:
                    result_.append(parser(part))
                return result_
            except ValueError:
                print(error)
    return result


parse_list_int = generate_list_parser("integer", int)
parse_list_int.__doc__ = """
    parse_float_list(prompt: str) -> result: List[int]; len(result) > 0

    Prompts the command line for a list of integers and returns it.
    If the input is not valid, this function keeps on trying again.
    """


parse_list_float = generate_list_parser("decimal", float)
parse_list_float.__doc__ = """
    parse_float_list(prompt: str) -> result: List[float]; len(result) > 0

    Prompts the command line for a list of floating-point numbers and returns it.
    If the input is not valid, this function keeps on trying again.
    """


def generate_matrix_parser(obj_desc: str, parser: Callable[[str], T]) -> Callable[[str], List[List[T]]]:
    """
    generate_matrix_parser(obj_desc: str, parser: Callable[[str], T]) -> parse_func: Callable[[str], List[List[T]]]

    Returns a parsing function that takes a prompt string and uses this function's argument error string and parser.
    """
    error1 = "The matrix must not be empty. Please provide at least one " + obj_desc
    error2 = "Please try again with a valid comma-separated " + obj_desc + " row"
    def result(prompt: str) -> List[T]:
        """
        result(prompt: str) -> result: List[T]; len(result) > 0

        Prompts the command line for a list of values and returns it.
        If the input is not valid, this function keeps on trying again.
        """
        print(prompt)
        print("Please input the matrix with each row on a separate line and the columns separated by commas."
              " Finish with an empty line.")
        print("### Begun parsing matrix ###")
        _result = []
        while True:
            try:
                input_str = input()
                if not input_str:
                    if _result:
                        break
                    else:
                        print(error1)
                split = input_str.split(",")
                row = [parser(part) for part in split]
                _result.append(row)
            except ValueError:
                print(error2)
        print("### Finished parsing matrix ###")
        return _result
    return result


parse_int_matrix = generate_matrix_parser("integer", int)
parse_int_matrix.__doc__ = """
    parse_int_matrix(prompt: int) -> result: List[List[int]]; len(result) > 0; len(x) > 0 ∀ x ∈ result

    Prompts the command line for a matrix of integers and returns it.
    If the matrix is not valid, this function keeps on trying again.
    """


parse_float_matrix = generate_matrix_parser("decimal", float)
parse_float_matrix.__doc__ = """
    parse_float_matrix(prompt: float) -> result: List[List[float]]; len(result) > 0; len(x) > 0 ∀ x ∈ result

    Prompts the command line for a matrix of floating-point numbers and returns it.
    If the matrix is not valid, this function keeps on trying again.
    """
