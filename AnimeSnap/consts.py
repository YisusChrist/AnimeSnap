"""Constants for the project."""

from pathlib import Path

from platformdirs import user_config_dir, user_log_dir

try:
    from importlib import metadata
except ImportError:  # for Python < 3.8
    import importlib_metadata as metadata  # type: ignore

__version__: str = metadata.version(__package__ or __name__)
__desc__: str = metadata.metadata(__package__ or __name__)["Summary"]
PACKAGE: str = metadata.metadata(__package__ or __name__)["Name"]
GITHUB: str = metadata.metadata(__package__ or __name__)["Home-page"]
AUTHOR: str = metadata.metadata(__package__ or __name__)["Author"]

CONFIG_PATH: str = user_config_dir(appname=PACKAGE, ensure_exists=True)
CONFIG_FILE: Path = Path(CONFIG_PATH).resolve() / f"{PACKAGE}.ini"
LOG_PATH: str = user_log_dir(appname=PACKAGE, ensure_exists=True)
LOG_FILE: Path = Path(LOG_PATH).resolve() / f"{PACKAGE}.log"
ICONS_PATH: Path = Path(__file__).parent.parent.resolve() / "icons"

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
