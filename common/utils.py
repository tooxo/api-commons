import re
from typing import Type, Optional, Union, Callable

from common.error import RegexMatchError, AsynchronousLibrariesNotFoundException
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
