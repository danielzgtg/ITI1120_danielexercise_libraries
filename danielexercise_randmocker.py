# Tools to mock random module

from collections import deque
from typing import Iterable, List
import random
from danielexercise_abstractmocker import MockerBase


def are_permutations(list1: List, list2: List) -> bool:
    """
    are_permutations(list1: List, list2: List) -> are_permutations: bool

    Return True iff the two lists are permutations of each other.
    This uses an alternative algorithm so that the items only need to implement __eq__.
    The simpler algorithm would just to sort and check if the list are equal.
    """
    l1 = list1.copy()
    l2 = list2.copy()
    for x in l1:
        try:
            l2.remove(x)
        except ValueError:
            return False
    return not bool(l2)


class RandomMocker(MockerBase):
    _randrange_buf: deque
    _shuffle_buf: deque

    def _init_buffers(self):
        self._randrange_buf = deque()
        self._shuffle_buf = deque()

    def _install_all(self, tester):
        self._install_randrange(tester)
        self._install_randint(tester)
        self._install_shuffle(tester)

    def _install_randrange(self, tester):
        def fake_randrange(start, stop=None, step=1):
            tester.assertTrue(self._randrange_buf)
            result = self._randrange_buf.popleft()
            tester.assertTrue(result in range(start, stop, step))
            return result
        self._backup_randrange = random.randrange
        random.randrange = fake_randrange

    def _install_randint(self, tester):
        def fake_randint(a, b):
            return random.randrange(a, b + 1)
        self._backup_randint = random.randint
        random.randint = fake_randint

    def _install_shuffle(self, tester):
        def fake_shuffle(x, random=None):
            tester.assertTrue(self._shuffle_buf)
            result = self._shuffle_buf.popleft()
            tester.assertTrue(are_permutations(x, result))
            x.clear()
            x.extend(result)
        self._backup_shuffle = random.shuffle
        random.shuffle = fake_shuffle

    def _uninstall_all(self):
        random.randrange = self._backup_randrange
        random.randint = self._backup_randint
        random.shuffle = self._backup_shuffle

    def expect_clean(self, tester):
        tester.assertFalse(self._randrange_buf)
        tester.assertFalse(self._shuffle_buf)

    def provide_randrange(self, rolls: Iterable[int]):
        self._randrange_buf.extend(rolls)

    def provide_shuffle(self, rolls: Iterable[List]):
        self._shuffle_buf.extend(rolls)
