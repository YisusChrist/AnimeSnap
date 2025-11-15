"""Main Python file containing the UI and functions"""

import sys

try:
    from rich.traceback import install
except ImportError:
    def install(*args, **kwargs) -> None:
        """Dummy install function if rich is not available."""
        pass

from AnimeSnap.cli import get_parsed_args
from AnimeSnap.gui import QApplication, Window


def main() -> None:
    """Main function"""
    args = get_parsed_args()
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
