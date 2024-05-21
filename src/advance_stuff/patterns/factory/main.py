import yaml
from actions import ActionFactory

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
