import yaml

def load_test_cases(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
