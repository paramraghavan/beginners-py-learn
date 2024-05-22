from abc import ABC, abstractmethod
from singleton_impl import Singleton

class BaseFactory(ABC):
    def __init__(self, params):
        self.params = params

    @abstractmethod
    def perform_action(self):
        pass


class PrintActionFactory(BaseFactory):
    def perform_action(self):
        message = self.params['message']
        print(message)
        Singleton.update_state('last_printed_message', message)

class SaveToFileFactory(BaseFactory):
    def perform_action(self):
        filename = self.params['filename']
        content = self.params['content']
        with open(filename, 'w+') as file:
            file.write(content)
        Singleton.update_state('last_saved_file', filename)
