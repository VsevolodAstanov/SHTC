import sys
import argparse


class CommandParser(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        # if nargs is not None:
        #     raise ValueError("nargs not allowed")
        super(CommandParser, self).__init__(option_strings, dest, **kwargs)


    def __call__(self, parser, namespace, values, option_string=None):
        print(namespace)
        setattr(namespace, self.dest, values)

def url_parm(string):
    """
        1. Get URL value and compare with existing values from yaml file
        2. If no one exists try to get value from DB
        3. ...
    """

    print(string)
    return str(string)

def main():
    """The main routine."""
    parser = argparse.ArgumentParser()
    commands = parser.add_mutually_exclusive_group(required=True)
    commands.add_argument('--get', dest="command", action='store_true')
    commands.add_argument('--view', dest="command", action='store_true')
    parser.add_argument('url', type=url_parm)
    args = parser.parse_args()

    print(args)


if __name__ == '__main__':
    main()