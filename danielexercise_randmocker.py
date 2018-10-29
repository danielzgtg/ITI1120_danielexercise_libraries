# Tools to mock random module

from collections import deque
from typing import Iterable, List
import random
from danielexercise_abstractmocker import MockerBase


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
            tester.assertTrue(sorted(x) == sorted(result))
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
