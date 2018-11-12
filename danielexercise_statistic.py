# Statistical utilities

from typing import Iterable, Dict, TypeVar, List, Tuple

T = TypeVar("T")


def histogram(data: Iterable[T]) -> Dict[T, int]:
    """
    histogram(data: Iterable[T]) -> histogram: Dict[T, [0..inf[]

    Returns the histogram of the argument data.
    A histogram is the number of occurrences of each item in the data.
    """
    result = {}
    for x in data:
        result[x] = result.get(x, 0) + 1
    return result


K = TypeVar("K")
V = TypeVar("V")


def _sorted_dict_pairs_helper(key_value_pair):
    (key, value) = key_value_pair
    return key


def sorted_dict_pairs(data: Dict[K, V]) -> List[Tuple[K, V]]:
    """
    sorted_dict_pairs(data: Dict[K, V]) -> sorted_key_value_pairs: List[(K, V):

    Returns the key-value pairs of the dictionary, sorted in key order.
    """
    return sorted(data.items(), key=_sorted_dict_pairs_helper)
