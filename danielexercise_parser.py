# Utilities for prompting the user for data
# Exports:
#   - parse_int(prompt: str) -> result: int
#   - parse_float(prompt: str) -> result: float
#   - parse_float_list(prompt: str) -> result: List[float]

from typing import List


def parse_int(prompt: str) -> int:
    """
    parse_int(prompt: int) -> result: int

    Prompts the command line for an integer and returns it.
    If the input is not a valid integer, this function keeps on trying again.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please try again with a valid integer")


def parse_float(prompt: str) -> float:
    """
    parse_float(prompt: float) -> result: float

    Prompts the command line for a floating-point number and returns it.
    If the input is not a valid floating-point number, this function keeps on trying again.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please try again with a valid decimal")


def parse_list_float(prompt: str) -> List[float]:
    """
    parse_float_list(prompt: float) -> result: List[float]; len(result) > 0

    Prompts the command line for a list of floating-point numbers and returns it.
    If the input is not a valid, this function keeps on trying again.
    """
    while True:
        try:
            input_str = input(prompt)
            split = input_str.split(",")
            result = []
            for part in split:
                result.append(float(part))
            return result
        except ValueError:
            print("Please try again with a valid comma-separated decimal list")
