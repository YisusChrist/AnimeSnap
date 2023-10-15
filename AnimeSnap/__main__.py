"""Main Python file containing the UI and functions"""
import cProfile
import sys

from PyQt6.QtWidgets import QApplication
from rich import print
from rich.traceback import install

from .consts import DEBUG, PROFILE
from .gui import App


def main():
    """Main function"""
    # Enable rich error formatting in debug mode
    install(show_locals=DEBUG)
    if DEBUG:
        print("[yellow]Debug mode is enabled[/]")

    app = QApplication(sys.argv)
    App().run()

    if PROFILE:
        print("[yellow]Profiling is enabled[/]")
        cProfile.run("sys.exit(app.exec())")
    else:
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
