"""conduct anime search"""


import urllib

import requests
from validators import url as validate_url

from .consts import API_URL, MAX_TIMEOUT


def search_anime(img_source: str, anilist_id: int = None) -> dict:
    """
    Conduct an anime search.

    Args:
        img_source (str): The image source.
        anilist_id (int, optional): The anilist id. Defaults to None.

    Returns:
        dict: The JSON response.

    Raises:
        requests.HTTPError: If the request fails.
        FileNotFoundError: If the file is not found.
    """
    if validate_url(img_source):
        # We know it is a URL
        url = API_URL + f"?url={urllib.parse.quote_plus(img_source)}"
        if anilist_id:
            url += f"&anilistInfo={anilist_id}"
        response = requests.get(url, timeout=MAX_TIMEOUT)
    else:
        # We know it is a file path
        with open(img_source, "rb") as file:
            data = file.read()
        response = requests.post(API_URL, files={"image": data}, timeout=MAX_TIMEOUT)

    response.raise_for_status()
    return response.json()
