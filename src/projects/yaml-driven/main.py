from singleton_impl import Singleton
from factory import PrintActionFactory,SaveToFileFactory


if __name__ == "__main__":
    singleton = Singleton()
    singleton.register_factory('print_action', PrintActionFactory)
    singleton.register_factory('save_to_file', SaveToFileFactory)

    singleton.parse_yaml('actions.yaml')
