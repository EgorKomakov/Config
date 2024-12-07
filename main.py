import json
import argparse


class ConfigurationError(Exception):
    pass


def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert JSON to configuration format.')
    parser.add_argument('input_file', type=str, help='/Users/egorkomakov/PycharmProjects/DZ3/.venv/info.json')
    parser.add_argument('output_file', type=str, help='/Users/egorkomakov/PycharmProjects/DZ3/.venv/output.cfg')
    return parser.parse_args()


def json_to_config(data):
    if isinstance(data, dict):
        return convert_dict(data)
    elif isinstance(data, list):
        return convert_list(data)


def convert_dict(d):
    lines = []
    for key, value in d.items():
        if isinstance(value, (int, float)):
            lines.append(f'const {key} = {value};')
        elif isinstance(value, str):
            if value.startswith('ord(') and value.endswith(')'):
                char = value[4:-1].strip('"')
                lines.append(f'const {key} = ord("{char}");')
            else:
                lines.append(f'const {key} = "{value}";')
        elif isinstance(value, list):
            lines.append(f"{key} = [{json_to_config(value)}];")
        elif isinstance(value, dict):
            operation_result = parse_operation(key, value)
            if operation_result:
                lines.append(operation_result)
    return "\n".join(lines)


def convert_list(lst):
    return ", ".join([convert_value(item) for item in lst])


def convert_value(value):
    if isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        if value.startswith('ord(') and value.endswith(')'):
            char = value[4:-1].strip('"')
            return f'ord("{char}")'
        return f'"{value}"'
    return str(value)


def parse_operation(key, operation):
    op_type = operation.get('operation')
    if op_type and 'left' in operation and 'right' in operation:
        left = operation['left']
        right = operation['right']
        left_str = convert_value(left)
        right_str = convert_value(right)
        if op_type == 'addition':
            return f'const {key} = {left_str} + {right_str};'
        elif op_type == 'subtraction':
            return f'const {key} = {left_str} - {right_str};'
        elif op_type == 'multiplication':
            return f'const {key} = {left_str} * {right_str};'
        elif op_type == 'division':
            return f'const {key} = {left_str} / {right_str};'
    return None


def main():
    args = parse_arguments()

    with open(args.input_file, 'r') as f:
        data = json.load(f)

    config_text = json_to_config(data)

    with open(args.output_file, 'w') as f:
        f.write(config_text)


if __name__ == "__main__":
    main()