# Base Class for Daniel's testing mockers

from abc import ABCMeta, abstractmethod


class MockerBase(object, metaclass=ABCMeta):

    # Do not override __init__()
    def __init__(self):
        self._init_buffers()

    # Do not override begin()
    def begin(self, tester):
        self._install_all(tester)

    @abstractmethod
    def _install_all(self, tester):
        pass

    @abstractmethod
    def _uninstall_all(self):
        pass

    # Do not override end()
    def end(self, tester):
        self._uninstall_all()
        self.expect_clean(tester)

    @abstractmethod
    def _init_buffers(self):
        pass

    @abstractmethod
    def expect_clean(self, tester):
        pass

