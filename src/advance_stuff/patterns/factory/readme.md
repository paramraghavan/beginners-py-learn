# Factory patten 

The factory pattern is useful for encapsulating the creation logic and can help in scenarios where the creation process
is complex or requires some form of configuration.

## Define the Base Class and Subclasses
First, define a base Action class and several subclasses, each implementing the execute method.

```python
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

```

## Implement FActory
Factory creates instances of the specific action classes based on the input type.

```python
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

```

## Parse the YAML File and Use the Factory

```python
import yaml

# Load and parse the YAML file
with open('actions.yaml', 'r') as file:
    actions_data = yaml.safe_load(file)

# Create and process actions using the factory
actions = []
for name, action_data in actions_data.items():
    action = ActionFactory.create_action(name, action_data)
    actions.append(action)

# Execute all actions
for action in actions:
    action.execute()

```