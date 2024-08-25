"""Main Python file containing the UI and functions"""

import cProfile
import sys
from typing import NoReturn

from PyQt6.QtWidgets import QApplication
from rich import print
from rich.traceback import install

from AnimeSnap.consts import DEBUG, PROFILE
from AnimeSnap.fluent_gui import Window
from AnimeSnap.gui import App


def app_fluent(app: QApplication) -> NoReturn:
    # qdarktheme.setup_theme("dark")
    window = Window()
    window.show()
    sys.exit(app.exec())


def app_qt(app: QApplication) -> NoReturn:
    ex = App()
    ex.run()
    sys.exit(app.exec())


def main() -> None:
    """Main function"""
    # Enable rich error formatting in debug mode
    install(show_locals=DEBUG)
    if DEBUG:
        print("[yellow]Debug mode is enabled[/]")

    app = QApplication(sys.argv)
    app_fluent(app)

    if PROFILE:
        print("[yellow]Profiling is enabled[/]")
        cProfile.run("sys.exit(app.exec())")
    else:
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
