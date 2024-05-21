Here we use python to parse yaml , each section of the yaml is an action which is processed by a class and all the
classes extend from action base class

```bash
pip install pyyaml
```

## Action base class
```python
class Action:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

    def execute(self):
        raise NotImplementedError("Subclasses should implement this!")

```

## Classes implemented to process yaml actions
```python
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


## the main class
```python
import yaml

# Define a function to create action instances based on the type
def create_action(name, action_data):
    action_type = action_data['type']
    parameters = action_data['parameters']
    
    if action_type == 'print':
        return PrintAction(name, parameters)
    elif action_type == 'save':
        return SaveAction(name, parameters)
    else:
        raise ValueError(f"Unknown action type: {action_type}")

# Load and parse the YAML file
with open('actions.yaml', 'r') as file:
    actions_data = yaml.safe_load(file)

# Create and process actions
actions = []
for name, action_data in actions_data.items():
    action = create_action(name, action_data)
    actions.append(action)

# Execute all actions
for action in actions:
    action.execute()

```