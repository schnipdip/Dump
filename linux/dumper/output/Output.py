from abc import ABC, abstractmethod


class Output(ABC):

    @abstractmethod
    def print(self, message, timeout: float = .5):
        pass
