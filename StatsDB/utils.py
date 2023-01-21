import re


def drop_nulls(txt_list: list):
    """
    Deletes all entries that are whitespace

    Args:
        txt (list): List to parse to clean up
    """
    result = []
    for txt in txt_list:
        if len(txt) > 0:
            result += [txt]
    return result


def is_list_subset(sublist: list,
                   superlist: list):
    """
    Checks if sublist is a subset of superlist

    Args:
        sublist (list): List to check
        superlist (list): The supposed superset

    Returns:
        bool: True if subset, False if
    """
    for entry in sublist:
        if entry not in superlist:
            return False

    return True


def parse_tags(txt):
    """
    Parses a tag string in format "#as #b#c" to give a list ['a', 'b', 'c']

    Args:
        txt (str): Tag inputs string

    Returns:
        list: List of tags
    """
    p = re.compile('#([^  #]*)')
    tags = set(p.findall(txt))
    tag_list = []
    for t in tags:
        if t:
            tag_list += [t]
    return tag_list
