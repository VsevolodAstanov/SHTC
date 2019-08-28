import sys
import argparse


class CommandParser(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(CommandParser, self).__init__(option_strings, dest, **kwargs)


    def __call__(self, parser, namespace, values, option_string=None):
        print(namespace)
        setattr(namespace, self.dest, values)

def url_parm(string):
    print(string)
    return "test"

def main(args=None):
    """The main routine."""
    parser = argparse.ArgumentParser()
    commands = parser.add_mutually_exclusive_group(required=True)
    commands.add_argument('get', dest="command", action=CommandParser)
    commands.add_argument('view', dest="command", action=CommandParser)
    #parser.add_argument('url', type=url_parm)

    parser.parse_args([])


if __name__ == '__main__':
    main()