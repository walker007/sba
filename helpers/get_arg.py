import sys


def get_arg(name, default=None):

    for arg in sys.argv:
        if arg.startswith('--'+name + "="):
            return arg.split("=")[1]
    return default
