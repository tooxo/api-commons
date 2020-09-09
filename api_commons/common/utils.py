import re
from typing import Type, Optional, Union, Callable

from api_commons.common.error import (
    RegexMatchError,
    AsynchronousLibrariesNotFoundException,
)
import pkg_resources


def regex_raise_check(
    regex: re.Pattern, test_string: str, error: Type[Exception]
):
    if not regex.match(test_string):
        raise error


def regex_search(
    regex: re.Pattern,
    test_string: str,
    group_no: Union[int, str] = 1,
    should_raise: bool = True,
) -> Optional[str]:
    match = regex.search(test_string).group(group_no)
    if not match and should_raise:
        raise RegexMatchError
    return match


def has_aiohttp(function) -> Callable:
    def wrapped(*args, **kwargs):
        try:
            pkg_resources.require(["aiohttp"])
        except pkg_resources.DistributionNotFound:
            raise AsynchronousLibrariesNotFoundException()
        return function(*args, **kwargs)

    return wrapped


def get_recursively(
    search_dict: dict, field: str, value_to_find: str, fields_found=None
):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    if not fields_found:
        fields_found = []

    for key, value in search_dict.items():
        if field == key and value_to_find == value:
            fields_found.append(search_dict)
        if isinstance(value, dict):
            fields_found = get_recursively(
                value, field, value_to_find, fields_found
            )
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(
                        item, field, value_to_find, fields_found
                    )
                    fields_found = more_results
    return fields_found
