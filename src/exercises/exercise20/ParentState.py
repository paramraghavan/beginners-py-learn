# Implementing hash-equals contract for a hashmap/dict
# First, let's define the class
class ParentState:
    def __init__(self, parent_id, state):
        self.parent_id = parent_id
        self.state = state

    def __hash__(self):
        return hash(self.parent_id)

    def __eq__(self, other):
        return self.parent_id == other.parent_id

# Create some sample data
my_dict = {}
my_dict[ParentState("P1", "active")] = "data1"
my_dict[ParentState("P2", "pending")] = "data2"


# Most efficient way
def find_by_parent_id(dictionary, parent_id):
    return dictionary.get(ParentState(parent_id, None))

# Usage
result = find_by_parent_id(my_dict, "P1")
if result:
    print("Found:", result)


# Method 1: Create a temporary ParentState object to search
parent_id_to_find = "P1"
result = my_dict.get(ParentState(parent_id_to_find, None))  # state doesn't matter for comparison

# Method 2: Search through keys
parent_id_to_find = "P1"
result = next((value for key, value in my_dict.items()
               if key.parent_id == parent_id_to_find), None)

# Method 3: Search and get both key and value
parent_id_to_find = "P1"
found_key = next((key for key in my_dict.keys()
                  if key.parent_id == parent_id_to_find), None)
if found_key:
    found_value = my_dict[found_key]
    found_state = found_key.state