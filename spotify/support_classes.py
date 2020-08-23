import json
from dataclasses import dataclass
from typing import Optional, List


class ExternalIds:
    @classmethod
    def from_api_response(cls, api_response: str):
        parsed_api_response: dict = json.loads(api_response)
        external_id = cls()
        for ob in parsed_api_response:
            setattr(external_id, ob, parsed_api_response[ob])
        return external_id


class ExternalUrls:
    spotify: str

    @classmethod
    def from_api_response(cls, api_response: str):
        parsed_api_response: dict = json.loads(api_response)
        external_url = cls()
        for ob in parsed_api_response:
            setattr(external_url, ob, parsed_api_response[ob])
        return external_url


@dataclass
class Image:
    url: str
    height: Optional[int]
    width: Optional[int]

    @classmethod
    def from_api_response(cls, api_response: str):
        parsed_api_response: dict = json.loads(api_response)
        return cls(
            url=parsed_api_response["url"],
            height=parsed_api_response["height"]
            if "height" in parsed_api_response
            else None,
            width=parsed_api_response["width"]
            if "width" in parsed_api_response
            else None,
        )


@dataclass
class Copyright:
    text: str
    type: str

    @classmethod
    def from_api_response(cls, api_response: str):
        parsed_api_response: dict = json.loads(api_response)
        return cls(
            text=parsed_api_response["text"], type=parsed_api_response["type"]
        )


@dataclass
class User:
    display_name: Optional[str]
    external_urls: ExternalUrls
    followers: int
    endpoint: str
    id: str
    images: List[Image]
    uri: str

    @classmethod
    def from_api_response(cls, api_response: str):
        parsed_api_response: dict = json.loads(api_response)
        return cls(
            display_name=parsed_api_response["display_name"]
            if "display_name" in parsed_api_response
            else None,
            external_urls=ExternalUrls.from_api_response(
                json.dumps(parsed_api_response["external_urls"])
            ),
            followers=parsed_api_response["followers"]["total"]
            if "followers" in parsed_api_response
            else None,
            endpoint=parsed_api_response["href"],
            id=parsed_api_response["id"],
            images=[
                Image.from_api_response(json.dumps(x))
                for x in parsed_api_response["images"]
            ]
            if "images" in parsed_api_response
            else None,
            uri=parsed_api_response["uri"],
        )
