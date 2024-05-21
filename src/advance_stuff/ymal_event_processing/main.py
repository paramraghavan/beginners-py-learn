import yaml
from action import Action, PrintAction, SaveAction


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
