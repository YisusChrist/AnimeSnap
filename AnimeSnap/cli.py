"""Command-line interface for the program."""

from argparse import Namespace

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
    parser, _ = setup_parser(
        package=PACKAGE,
        description=DESC,
        version=VERSION,
        theme=ArgparseColorThemes.PRINCE,
    )

    return parser.parse_args()
