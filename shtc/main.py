import sys
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    get_parser = subparsers.add_parser('--get')
    view_parser = subparsers.add_parser('--view')
    get_parser.add_argument('name')
    view_parser.add_argument('name')

    # parser.add_argument('--get', action='store_true', default=False)
    # parser.add_argument('--view', action='store_true', default=False)

    return parser

def main():
    """
    --get Get Data via HTTP Request
    --view Get Data from DB if data exist
    :return: Count of tags
    """

    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    print(namespace)

    if namespace['--get']:
        print("--get")
    elif namespace['--view']:
        print("--view")
    else:
        print("Run GUI")


if __name__ == '__main__':
  main()