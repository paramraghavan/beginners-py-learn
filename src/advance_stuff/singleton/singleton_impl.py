import yaml

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    _state = {}
    def __init__(self):
        self.factory_classes = {}

    @staticmethod
    def update_state(key, value):
        Singleton._state[key] = value
        print(f"State updated: {key} = {value}")

    @staticmethod
    def get_state(self, key):
        return Singleton._state.get(key, None)


    def register_factory(self, action, factory_class):
        self.factory_classes[action] = factory_class

    def parse_yaml(self, yaml_file):
        with open(yaml_file, 'r') as file:
            actions = yaml.safe_load(file)
            for action in actions:
                factory_class = self.factory_classes.get(action['type'])
                if factory_class:
                    factory_instance = factory_class(action['params'])
                    factory_instance.perform_action()
                else:
                    print(f"Unknown action type: {action['type']}")
