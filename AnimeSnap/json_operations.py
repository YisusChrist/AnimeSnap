"""Handle JSON to str conversion and write JSON to an external file."""

import json
from functools import partial


def format_entry(entry: dict, include_all_details: bool) -> str:
    """
    Format a single entry in the JSON result.

    Args:
        entry (dict): A single entry in the JSON result.
        include_all_details (bool): Whether to include all details.

    Returns:
        str: The formatted entry.
    """
    formatted_data = ""

    items = entry.items()
    if not include_all_details:
        items = filter(
            lambda item: item[0]
            not in [
                "anilist",
                "video",
                "image",
            ],
            items,
        )

    for key, value in items:
        if key == "anilist" and isinstance(entry[key]) is dict:
            for k, v in entry[key].items():
                formatted_data += f"{k.capitalize()}: {v}\n"
        elif key == "similarity":
            formatted_data += f"{key.capitalize()}: {value * 100:.2f}%\n"
        else:
            formatted_data += f"{key.capitalize()}: {value}\n"

    return formatted_data


def json_to_tabular(data: dict, include_all_details: bool = False) -> str:
    """
    Convert the JSON result to a tabular format.

    Args:
        data (dict): The JSON containing the search result.
        include_all_details (bool, optional): Whether to include all details.
            Defaults to False.

    Returns:
        str: The tabular format of the JSON result.
    """
    format_entry_with_iad = partial(
        format_entry, include_all_details=include_all_details
    )
    formatted_data_list = map(format_entry_with_iad, data)
    formatted_data = "\n\n".join(formatted_data_list)
    return formatted_data


def save_to_json(file_name: str, data: dict) -> None:
    """
    Save the JSON data to a file.

    Args:
        file_name (str): The name of the file to save the JSON data to.
        data (dict): The JSON data to save.

    Raises:
        Exception: An error occurred while saving the JSON data.
    """
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
