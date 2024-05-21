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


class ActionFactory:
    @staticmethod
    def create_action(name, action_data):
        action_type = action_data['type']
        parameters = action_data['parameters']

        if action_type == 'print':
            return PrintAction(name, parameters)
        elif action_type == 'save':
            return SaveAction(name, parameters)
        else:
            raise ValueError(f"Unknown action type: {action_type}")
