from hashlib import sha256

import requests

from typing import List, Tuple
from html.parser import HTMLParser

from etest_worker.exceptions import (
    PresentationParsingError,
    PresentationNotFound,
)


class PresentationParses(HTMLParser):
    def __init__(self, *args, **kwargs):
        self._slides: List[str] = []
        self._hash = sha256()
        super(PresentationParses, self).__init__(*args, **kwargs)

    def handle_starttag(self, tag, attrs):
        if tag == "slide":
            for key, value in attrs:
                if key == "data":
                    self._slides.append(value)
                    self._hash.update(value.encode("utf-8"))

    def parse(self, data: str) -> Tuple[List[str], str]:
        self._slides = []
        self._hash = sha256()

        super(PresentationParses, self).feed(data)

        if len(self._slides) < 1:
            raise PresentationNotFound()

        return self._slides, self._hash.hexdigest()

    def error(self, message):
        pass


presentation_parser = PresentationParses()


def get_presentation(
    url: str, session: requests.Session
) -> Tuple[List[str], str]:
    presentation_text = session.get(url).text
    try:
        return presentation_parser.parse(presentation_text)
    except Exception as exc:
        raise PresentationParsingError(exc)
