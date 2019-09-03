import sys

from shtc.shtc import TagCounter
from shtc.gui import run_gui_app


def main():
    tc = TagCounter()
    args = tc.get_console_args()
    ns = sys.argv
    if len(ns) > 1:
        if args.get:
            logging.debug('[CONSOLE] Get Data using HTTP Request')
            tc.get_http_data()
        elif args.view:
            logging.debug('[CONSOLE] Get Data using DB')
            tc.get_db_data()
        elif args.delete:
            logging.debug('[CONSOLE] Delete Data from DB')
            tc.delete_db_data()
            sys.exit()

        tc.display()
    else:
        run_gui_app()


if __name__ == '__main__':
    main()
