"""Constants for the project."""
from pathlib import Path

from platformdirs import user_config_dir, user_log_dir

from . import PACKAGE, __desc__, __version__

NAME = PACKAGE  # Path(__file__).name.split(".")[0]
CONFIG_PATH = user_config_dir(appname=NAME, ensure_exists=True)
CONFIG_FILE = Path(CONFIG_PATH).resolve() / f"{NAME}.ini"
LOG_PATH = user_log_dir(appname=NAME, ensure_exists=True)
LOG_FILE = Path(LOG_PATH).resolve() / f"{NAME}.log"
ICONS_PATH = Path(__file__).parent.parent.resolve() / "icons"
VERSION = __version__
DESC = __desc__

X = 100
Y = 100
WIDTH = 750
HEIGHT = 800
ICON_SIZE = 23

API_URL = "https://api.trace.moe/search"
MAX_TIMEOUT = 10

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

DEBUG = False
PROFILE = False
