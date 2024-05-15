import yaml

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def print_matrices(data):
    for layer_name, matrix in data.items():
        print(f"{layer_name}:")
        for row in matrix:
            print(row)
        print()

# Load the YAML file
yaml_data = load_yaml('sample.yaml')

# Print matrices
print_matrices(yaml_data)
