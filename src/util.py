from getpass import getpass
import os
import sys


def get_env_var(varName, prompt):
    # Read the <varName> environment variable,
    # or ask for it if none is set.

    token = os.environ.get(varName)
    if not token:
        token = getpass(prompt)

    return token


def print_inplace(line):
    sys.stdout.write('\r' + line)
    sys.stdout.flush()
