def read_yaml_file(file_path):
    """Read a YAML file and return its contents."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return None

def write_yaml_file(file_path, data):
    """Write data to a YAML file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
    except Exception as e:
        print(f"Error writing to YAML file: {e}")

def file_exists(file_path):
    """Check if a file exists."""
    return Path(file_path).is_file()