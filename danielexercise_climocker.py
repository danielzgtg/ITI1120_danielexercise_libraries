# Tools to mock print() and input()


from collections import deque
from typing import Iterable
import builtins
from danielexercise_abstractmocker import MockerBase


class CLIMocker(MockerBase):
    _input_buf: deque
    _output_buf: deque
    _output_incomplete: str

    def _init_buffers(self):
        self._input_buf = deque()
        self._output_buf = deque()
        self._output_incomplete = ""

    def _install_all(self, tester):
        self._install_print(tester)
        self._install_input(tester)

    def _install_print(self, tester):
        def fake_print(*args, sep=" ", end="\n", file=None, flush=False):
            body = sep.join(map(str, args))
            if end == "\n":
                self._output_buf.append(self._output_incomplete + body)
                self._output_incomplete = ""
            else:
                self._output_incomplete += body + end
                if "\n" in self._output_incomplete:
                    split = self._output_incomplete.split("\n")
                    self._output_incomplete = split[-1]
                    for complete in split[:-1]:
                        self._output_buf.append(complete)
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
                split = take.split("\n")
                take = split[0]
                for extra in reversed(split[1:]):
                    self._output_buf.appendleft(extra)
            tester.assertEqual(line, take)
