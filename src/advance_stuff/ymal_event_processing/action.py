
class Action:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

    def execute(self):
        raise NotImplementedError("Subclasses should implement this!")


class PrintAction(Action):
    def execute(self):
        message = self.parameters.get('message', '')
        print(f"PrintAction: {message}")

class SaveAction(Action):
    def execute(self):
        file_path = self.parameters.get('file_path', 'default.txt')
        content = self.parameters.get('content', '')
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"SaveAction: Content saved to {file_path}")