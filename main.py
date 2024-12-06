import json
import argparse
import re

class ConfigurationError(Exception):
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert JSON to custom configuration language')
    parser.add_argument('input_file', type=str, help='/Users/egorkomakov/PycharmProjects/DZ3/.venv/info.json')
    parser.add_argument('output_file', type=str, help='/Users/egorkomakov/PycharmProjects/DZ3/.venv/output.cfg')
    return parser.parse_args()

def json_to_config(data):
    if isinstance(data, dict):
        return convert_dict(data)
    elif isinstance(data, list):
        return convert_list(data)
    else:
        raise ConfigurationError(f"Unsupported data type: {type(data)}")

def convert_dict(d):
    lines = []
    for key, value in d.items():
        # Validate key syntax
        if not re.match(r'^[A-Z]+$', key):
            raise ConfigurationError(f"Invalid name: {key}")
        # Handle constants
        if isinstance(value, (int, float, str)):
            lines.append(f'const {key} = {convert_value(value)}')
        elif isinstance(value, (list, dict)):
            lines.append(f"{key} = ({json_to_config(value)})")
        else:
            raise ConfigurationError(f"Unsupported value type for key '{key}': {type(value)}")
    return "\n".join(lines)

def convert_list(lst):
    return ", ".join([convert_value(item) for item in lst])

def convert_value(value):
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        return f"({convert_list(value)})"
    else:
        raise ConfigurationError(f"Unsupported value type: {type(value)}")

def main():
    args = parse_arguments()

    # Read input JSON
    with open(args.input_file, 'r') as infile:
        try:
            json_data = json.load(infile)
            config_output = json_to_config(json_data)
        except ValueError as e:
            raise ConfigurationError(f"Invalid JSON data: {e}")

    # Write output to configuration file
    with open(args.output_file, 'w') as outfile:
        outfile.write(config_output)

if __name__ == '__main__':
    main()