"""Command-line interface for the program."""

import sys
from argparse import Namespace

if sys.version_info > (3, 5):
    from core_helpers.cli import ArgparseColorThemes, setup_parser

from AnimeSnap.consts import PACKAGE
from AnimeSnap.consts import __desc__ as DESC
from AnimeSnap.consts import __version__ as VERSION


def get_parsed_args() -> Namespace:
    """
    Parse and return command-line arguments.

    Returns:
        The parsed arguments as an argparse.Namespace object.
    """
    if sys.version_info > (3, 5):
        parser, _ = setup_parser(
            package=PACKAGE,
            description=DESC,
            version=VERSION,
            theme=ArgparseColorThemes.PRINCE,
        )
        return parser.parse_args()

    from argparse import ArgumentParser

    parser = ArgumentParser(description=DESC, add_help=False)

    misc_group = parser.add_argument_group("Miscellaneous Options")
    # Help
    misc_group.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit."
    )
    # Verbose
    misc_group.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Show log messages on screen. Default is False.",
    )
    # Debug
    misc_group.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Activate debug logs. Default is False.",
    )
    # Version
    misc_group.add_argument(
        "-V",
        "--version",
        action="version",
        help="Show version number and exit.",
        version="%(prog)s " + VERSION,
    )

    return parser.parse_args()
