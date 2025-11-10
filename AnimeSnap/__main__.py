"""Main Python file containing the UI and functions"""

import sys
from argparse import Namespace

from rich.traceback import install

from AnimeSnap.cli import get_parsed_args
from AnimeSnap.gui import QApplication, Window


def main() -> None:
    """Main function"""
    args: Namespace = get_parsed_args()
    install(show_locals=args.debug)

    App = QApplication(sys.argv)
    if args.debug:
        print("Debug mode is ON")
        # Message displayed about the Qt
        App.aboutQt()

    Window().run()
    sys.exit(App.exec())


if __name__ == "__main__":
    main()
