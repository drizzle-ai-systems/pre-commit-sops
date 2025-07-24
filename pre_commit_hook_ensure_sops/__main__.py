#!/usr/bin/env python3
"""
Validate if given list of files are encrypted with sops.
"""
from argparse import ArgumentParser
import json
from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError
import sys
import re

yaml = YAML(typ='safe')

def is_encrypted_value(data):
    """
    Recursively checks if a data structure is fully encrypted.
    All leaf strings must start with 'ENC['.
    """
    if isinstance(data, dict):
        return all(is_encrypted_value(v) for v in data.values())
    if isinstance(data, list):
        return all(is_encrypted_value(i) for i in data)
    if isinstance(data, str):
        return data.startswith('ENC[')
    # Allow other types like bools, numbers to pass.
    return True

def find_unencrypted_keys(data, pattern_re):
    """
    Finds top-level keys in the data that match the pattern
    but have unencrypted values.
    """
    unencrypted_keys = []
    for key, value in data.items():
        if key == 'sops':
            continue
        # Check if the top-level key matches the regex pattern
        if pattern_re.search(key):
            # If the key matches, its entire value structure must be encrypted
            if not is_encrypted_value(value):
                unencrypted_keys.append(key)
    return unencrypted_keys

def check_file(filename, pattern=None):
    """
    Check if a file has been encrypted properly with sops,
    optionally checking only keys that match a regex pattern.
    """
    try:
        with open(filename, 'r') as f:
            if filename.endswith(('.yaml', '.yml')):
                doc = yaml.load(f)
            else:
                doc = json.load(f)
    except (ParserError, json.JSONDecodeError, FileNotFoundError) as e:
        return False, f"{filename}: Error reading or parsing file: {e}"

    if 'sops' not in doc:
        return False, f"{filename}: sops metadata key not found. The file is not encrypted."

    # If no pattern is provided, perform a simple check on the whole file.
    if not pattern:
        doc.pop('sops')
        if not is_encrypted_value(doc):
             return False, f"{filename}: Unencrypted values found in file."
        return True, f"{filename}: Valid encryption."

    # If a pattern is provided, compile it and check only matching keys.
    try:
        pattern_re = re.compile(pattern)
    except re.error as e:
        return False, f"Invalid regex pattern '{pattern}': {e}"

    unencrypted = find_unencrypted_keys(doc, pattern_re)

    if unencrypted:
        msg = f"{filename}: Unencrypted values found for keys matching pattern '{pattern}': {', '.join(unencrypted)}"
        return False, msg

    return True, f"{filename}: Valid encryption for keys matching pattern '{pattern}'."

def main():
    # 'pre-commit' passes the filenames as positional arguments.
    # We add our own optional '--pattern' argument.
    argparser = ArgumentParser(
        description="Check for sops encryption, optionally against a key pattern."
    )
    argparser.add_argument('filenames', nargs='+', help="Files to check")
    argparser.add_argument('--pattern', help='Regex pattern to match keys that should be encrypted')
    args = argparser.parse_args()

    exit_code = 0
    for filename in args.filenames:
        is_valid, message = check_file(filename, pattern=args.pattern)
        print(message)
        if not is_valid:
            exit_code = 1

    return exit_code

if __name__ == '__main__':
    sys.exit(main())