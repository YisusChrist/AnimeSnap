import inspect

from filetype.types import image  # type: ignore


def get_image_extensions():
    """
    Get a list of image extensions from the filetype module.

    Returns:
        list: A list of image extensions.
    """
    # Get a list of class names defined in the module
    class_names = [
        name for name, obj in inspect.getmembers(image) if inspect.isclass(obj)
    ]

    # Extract the different classes names from the Image class
    return ["*" + c.lower() for c in class_names]
