import re
from typing import Callable, TYPE_CHECKING

from common.error import InvalidUrlError
from common.utils import regex_raise_check

if TYPE_CHECKING:
    from spotify import SpotifyApi

SPOTIFY_URL_REGEX = re.compile(
    r"^(http(s)?://)?"
    r"(open\.|play\.)"
    r"spotify\.com/(user/.{,32}/)?(playlist|track|album|artist)/"
    r"(?P<id>[A-Za-z0-9]{22,23})(\?|$)(si=.{22,23})?$",
    re.IGNORECASE,
)
SPOTIFY_TRACK_REGEX = re.compile(
    r"^(http(s)?://)?"
    r"(open\.|play\.)"
    r"spotify\.com/(user/.{,32}/)?track/"
    r"(?P<id>[A-Za-z0-9]{22,23})(\?|$)(si=.{22,23})?$",
    re.IGNORECASE,
)
SPOTIFY_PLAYLIST_REGEX = re.compile(
    r"^(http(s)?://)?"
    r"(open\.|play\.)"
    r"spotify\.com/(user/.{,32}/)?playlist/"
    r"(?P<id>[A-Za-z0-9]{22,23})(\?|$)(si=.{22,23})?$",
    re.IGNORECASE,
)
SPOTIFY_ARTIST_REGEX = re.compile(
    r"^(http(s)?://)?"
    r"(open\.|play\.)"
    r"spotify\.com/(user/.{,32}/)?artist/"
    r"(?P<id>[A-Za-z0-9]{22,23})(\?|$)(si=.{22,23})?$",
    re.IGNORECASE,
)
SPOTIFY_ALBUM_REGEX = re.compile(
    r"^(http(s)?://)?"
    r"(open\.|play\.)"
    r"spotify\.com/(user/.{,32}/)?album/"
    r"(?P<id>[A-Za-z0-9]{22,23})(\?|$)(si=.{22,23})?$",
    re.IGNORECASE,
)


class InvalidSpotifyUrlError(InvalidUrlError):
    """
    Raised, when a given spotify url was invalid
    """

    pass


def validate_spotify(url: str) -> None:
    """
    Raises [InvalidSpotifyUrlError], when [url] is an invalid spotify url
    @param url: Url to validate
    """
    regex_raise_check(SPOTIFY_URL_REGEX, url, InvalidSpotifyUrlError)


def validate_spotify_track(url: str) -> None:
    """
    Raises [InvalidSpotifyUrlError], when [url] is an invalid spotify track url
    @param url: Url to validate
    """
    regex_raise_check(SPOTIFY_TRACK_REGEX, url, InvalidSpotifyUrlError)


def validate_spotify_playlist(url: str) -> None:
    """
    Raises [InvalidSpotifyUrlError], when [url] is an invalid spotify playlist
    url
    @param url: Url to validate
    """
    regex_raise_check(SPOTIFY_PLAYLIST_REGEX, url, InvalidSpotifyUrlError)


def validate_spotify_artist(url: str) -> None:
    """
    Raises [InvalidSpotifyUrlError], when [url] is an invalid spotify artist url
    @param url: Url to validate
    """
    regex_raise_check(SPOTIFY_ARTIST_REGEX, url, InvalidSpotifyUrlError)


def validate_spotify_album(url: str) -> None:
    """
    Raises [InvalidSpotifyUrlError], when [url] is an invalid spotify album url
    @param url: Url to validate
    """
    regex_raise_check(SPOTIFY_ALBUM_REGEX, url, InvalidSpotifyUrlError)


def decorator(validation_function: Callable):
    """
    Decorator to wrap all validation functions
    @param validation_function: one of the functions above
    @return:
    """

    def decorator_wrapper(fun: Callable):
        def function_wrapper(arg1: "SpotifyApi", url: str):
            validation_function(url)
            return fun(arg1, url)

        return function_wrapper

    return decorator_wrapper
