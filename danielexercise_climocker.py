# Tools to mock print() and input()


from collections import deque
from typing import Iterable
import builtins
from danielexercise_abstractmocker import MockerBase


class CLIMocker(MockerBase):
    _input_buf: deque
    _output_buf: deque

    def _init_buffers(self):
        self._input_buf = deque()
        self._output_buf = deque()

    def _install_all(self, tester):
        self._install_print(tester)
        self._install_input(tester)

    def _install_print(self, tester):
        def fake_print(*args):
            self._output_buf.append(" ".join(map(str, args)))
        self._backup_print = builtins.print
        builtins.print = fake_print

    def _install_input(self, tester):
        def fake_input(prompt=""):
            print(prompt)
            if not self._input_buf:
                raise EOFError
            return self._input_buf.popleft()
        self._backup_input = builtins.input
        builtins.input = fake_input

    def _uninstall_all(self):
        builtins.print = self._backup_print
        builtins.input = self._backup_input

    def expect_clean(self, tester):
        tester.assertFalse(self._input_buf)
        tester.assertFalse(self._output_buf)

    def provide_input(self, lines: Iterable[str]):
        self._input_buf.extend(lines)

    def expect_output(self, tester, expected_lines: Iterable[str]):
        for line in expected_lines:
            tester.assertTrue(self._output_buf)
            take = self._output_buf.popleft()
            if "\n" in take:
                take2 = take.split("\n")
                take = take2[0]
                for extra in reversed(take2[1:]):
                    self._output_buf.appendleft(extra)
            tester.assertEqual(line, take)
