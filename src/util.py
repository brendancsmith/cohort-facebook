from getpass import getpass
import os

def get_env_var(varName, prompt):
    # Read the <varName> environment variable,
    # or ask for it if none is set.

    token = os.environ.get(varName)
    if not token:
        token = getpass(prompt)

    return token
