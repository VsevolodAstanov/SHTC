import sys
# from shtc.logger import Logger
from shtc.shtc import TagCounter
from shtc.gui import run_gui_app


def main():
    tc = TagCounter()
    args = tc.get_console_args()
    ns = sys.argv
    if len(ns) > 1:
        if args.get:
            tc.get_http_data()
        elif args.view:
            tc.get_db_data()
        elif args.delete:
            tc.delete_db_data()
            sys.exit()

        tc.display()
    else:
        run_gui_app()


if __name__ == '__main__':
    main()
