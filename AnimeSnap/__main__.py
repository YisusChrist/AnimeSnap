"""Main Python file containing the UI and functions"""

import sys
from argparse import Namespace

from PyQt6.QtWidgets import QApplication
from rich.traceback import install

from AnimeSnap.cli import get_parsed_args
from AnimeSnap.gui import App


def main() -> None:
    """Main function"""
    args: Namespace = get_parsed_args()
    install(show_locals=args.debug)

    app = QApplication(sys.argv)
    App().run()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
