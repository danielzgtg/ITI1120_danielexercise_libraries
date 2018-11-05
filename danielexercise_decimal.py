# Infinite-precision decimal utilities
# Exports:
#   - Decimal
#     - Decimal() -> Decimal
#     - inherit_decimal_str(decimal_str: str) -> None
#     - __add__(other: Decimal) -> Decimal
#     - __radd__(other: Decimal) -> Decimal
#     - __sub__(other: Decimal) -> Decimal
#     - __mul__(other: Decimal) -> Decimal
#     - __lt__(other: Decimal) -> bool
#     - __le__(other: Decimal) -> bool
#     - __eq__(other: Decimal) -> bool
#     - __ne__(other: Decimal) -> bool
#     - __ge__(other: Decimal) -> bool
#     - __gt__(other: Decimal) -> bool
#     - __repr__() -> str
#   - decimal(toconvert: Any) -> Decimal
#   - parse_decimal(prompt: str) -> Decimal

from __future__ import annotations


#LIBRARY
def _order_of_magnitude_to_int(order_of_magnitude: int) -> int:
    """
    order_of_magnitude_to_int(order_of_magnitude: int) -> multiplier: int

    Returns 10 to the power of order_of_magnitude.
    """
    if order_of_magnitude == 0:
        return 1
    elif order_of_magnitude < 0:
        raise ValueError
    else:
        result = 1
        for _ in range(order_of_magnitude):
            result *= 10
        return result


class Decimal:
    base: int
    order_of_magnitude: int

    def __init__(self) -> None:
        self.base = 0
        self.order_of_magnitude = 0

    def inherit_decimal_str(self, decimal_str: str) -> None:
        """
        inherit_decimal_str(decimal_str: str) -> None

        Makes this Decimal represent the decimal string.
        Raises ValueError if the string cannot be represented as valid decimal.
        """
        point_idx = decimal_str.rfind(".")
        if point_idx < 0:
            self._inherit_int(decimal_str)
            return

        before = decimal_str[:point_idx]
        after = decimal_str[point_idx+1:]
        if after == "":
            self._inherit_int(before)
            return

        mag = len(after)
        multiplier = _order_of_magnitude_to_int(mag)
        before_int = int(before) * multiplier
        after_int = int(after)

        if before_int >= 0:
            base = before_int + after_int
        else:
            base = before_int - after_int

        self.base = base
        self.order_of_magnitude = mag

        self._simplify()

    def _inherit_int(self, int_str: str) -> None:
        """
        inherit_int(self, int_str: str) -> None

        Makes this decimal represent the parameter int.
        _simplify() MUST be called before returning out of the module.
        """
        self.base = int(int_str)
        self.order_of_magnitude = 0

    def _ensure_precision(self, other: Decimal) -> None:
        """
        _ensure_precision(self, other: Decimal) -> None

        Makes this Decimal have the same magnitude as the other Decimal.
        This is done by increasing the smallest magnitude.
        _simplify() MUST be called before returning out of the module.
        """
        if self.order_of_magnitude == other.order_of_magnitude:
            return
        if self.order_of_magnitude > other.order_of_magnitude:
            target_mag = self.order_of_magnitude
            to_fix = other
        else:
            target_mag = other.order_of_magnitude
            to_fix = self
        mag_diff = target_mag - to_fix.order_of_magnitude
        multiplier = _order_of_magnitude_to_int(mag_diff)
        to_fix.base *= multiplier
        to_fix.order_of_magnitude = target_mag

    def _simplify(self) -> None:
        """
        _simplify(self) -> None

        Simplifies this Decimal until the magnitude of its base is as small as possible by increasing the magnitude.
        """
        if self.base == 0:
            self.order_of_magnitude = 0
            return
        while self.base % 10 == 0:
            self.base //= 10
            self.order_of_magnitude -= 1

    def _addsub_op_prepare(self, other: Decimal) -> Decimal:
        """
        _addsub_op_prepare(self, other: Decimal) -> buffer: Decimal

        Does half of the logic for _add and _sub.
        """
        if not isinstance(other, Decimal):
            raise TypeError
        self._ensure_precision(other)
        result = Decimal()
        result.order_of_magnitude = self.order_of_magnitude
        result.base = self.base
        return result

    def _op_simplify(self, other: Decimal, buffer: Decimal) -> None:
        """
        _op_simplify(self, other: Decimal, buffer: Decimal) -> None

        Re-simplifies Decimal objects whose precisions have been increased for other operations.
        """
        self._simplify()
        other._simplify()
        buffer._simplify()

    def _mul_op_prepare(self, other: Decimal) -> Decimal:
        """
        _mul_op_prepare(self, other: Decimal) -> buffer: Decimal

        Does half of the logic for _mul.
        """
        if not isinstance(other, Decimal):
            raise TypeError
        result = Decimal()
        result.order_of_magnitude = self.order_of_magnitude + other.order_of_magnitude
        result.base = self.base
        return result

    def __add__(self, other: Decimal) -> Decimal:
        result = self._addsub_op_prepare(other)
        result.base += other.base
        self._op_simplify(other, result)
        return result

    def __radd__(self, other: Decimal) -> Decimal:
        result = self._addsub_op_prepare(other)
        result.base += other.base
        self._op_simplify(other, result)
        return result

    def __sub__(self, other: Decimal) -> Decimal:
        result = self._addsub_op_prepare(other)
        result.base -= other.base
        self._op_simplify(other, result)
        return result

    def __mul__(self, other: Decimal) -> Decimal:
        result = self._mul_op_prepare(other)
        result.base *= other.base
        result._simplify()
        return result

    def __repr__(self) -> str:
        return "{DanielDecimal " + str(self.base) + " / 10**" + str(self.order_of_magnitude) + " }"

    def __lt__(self, other: Decimal) -> bool:
        diff = self - other
        return diff.base < 0

    def __le__(self, other: Decimal) -> bool:
        diff = self - other
        return diff.base <= 0

    def __eq__(self, other: Decimal) -> bool:
        diff = self - other
        return diff.base == 0

    def __ne__(self, other: Decimal) -> bool:
        diff = self - other
        return diff.base != 0

    def __ge__(self, other: Decimal) -> bool:
        diff = self - other
        return diff.base >= 0

    def __gt__(self, other: Decimal) -> bool:
        diff = self - other
        return diff.base > 0


def decimal(toconvert) -> Decimal:
    """
    decimal(toconvert: Any) -> result: Decimal

    Returns the passed parameter magically converted into a decimal.
    If this fails, any Error might be raised.
    """
    decimal_str = str(toconvert)
    result = Decimal()
    result.inherit_decimal_str(decimal_str)
    return result


def parse_decimal(prompt: str) -> Decimal:
    """
    parse_decimal(prompt: float) -> result: Decimal

    Prompts the command line for a decimal and returns it.
    If the input is not a valid decimal, this function keeps on trying again.
    """
    while True:
        try:
            return decimal(input(prompt))
        except ValueError:
            print("Please try again with a valid decimal")
