from abc import ABC, abstractmethod

class BaseFactory(ABC):
    def __init__(self, params):
        self.params = params

    @abstractmethod
    def perform_action(self):
        pass


class PrintActionFactory(BaseFactory):
    def perform_action(self):
        print(self.params['message'])

class SaveToFileFactory(BaseFactory):
    def perform_action(self):
        with open(self.params['filename'], 'w') as file:
            file.write(self.params['content'])
