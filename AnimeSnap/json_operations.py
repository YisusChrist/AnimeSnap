"""Handle JSON to str conversion and write JSON to an external file."""

import json
from functools import partial


def format_entry(entry, include_all_details: bool) -> str:
    """
    Format a single entry in the JSON result.

    Args:
        entry (dict[str, str | int]): A single entry in the JSON result.
        include_all_details (bool): Whether to include all details.

    Returns:
        str: The formatted entry.
    """
    excluded_keys = {"anilist", "video", "image"}

    items = (
        entry.items()
        if include_all_details
        else {k: v for k, v in entry.items() if k not in excluded_keys}
    )

    lines = []
    for key, value in items.items():
        if key == "anilist" and isinstance(entry[key], dict):
            lines.extend(k.capitalize() + ":" + v for k, v in value.items())
        elif key == "similarity":
            lines.append(key.capitalize() + ":" + str(value * 100) + "%")
        else:
            lines.append(key.capitalize() + ":" + str(value))

    return "\n".join(lines)


def json_to_tabular(
    data, include_all_details: bool = False
) -> str:
    """
    Convert the JSON result to a tabular format.

    Args:
        data (dict[str, str | int]): The JSON containing the search result.
        include_all_details (bool, optional): Whether to include all details.
            Defaults to False.

    Returns:
        str: The tabular format of the JSON result.
    """
    format_entry_with_iad = partial(
        format_entry, include_all_details=include_all_details
    )
    formatted_data_list = map(format_entry_with_iad, data)
    return "\n\n".join(formatted_data_list)


def save_to_json(file_name: str, data) -> None:
    """
    Save the JSON data to a file.

    Args:
        file_name (str): The name of the file to save the JSON data to.
        data (dict[str, str | int]): The JSON data to save.

    Raises:
        Exception: An error occurred while saving the JSON data.
    """
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
