import base64
from io import BytesIO
from typing import List, Iterator, BinaryIO

from PIL import Image
from flask import current_app

from etest_download.transformer.base import BaseTransformer


class PresentationToPdf(BaseTransformer):
    """Transforms presentation to pdf format"""

    @staticmethod
    def _base64_to_bytes_io(b64: str) -> BytesIO:
        bytes_io = BytesIO(base64.b64decode(b64))
        bytes_io.seek(0)
        return bytes_io

    @classmethod
    def _base64_to_images(cls, slides: List[str]) -> Iterator[Image.Image]:
        """
        Transforms base64 images to PIL.Image.Image

        :param slides: list of strings with base64 encoded images
        :return: Iterator of PIL.Image.Image objects
        """
        for slide in slides:
            try:
                img: Image.Image = Image.open(cls._base64_to_bytes_io(slide))
                img.convert("RGB")
            except Exception as exc:
                current_app.logger.warning(
                    "Error during slide parsing: %s", exc
                )
            else:
                yield img

    @classmethod
    def transform(cls, slides: List[str]) -> BinaryIO:
        """
        Transforms base64 images to PDF

        :param slides: list of strings with base64 encoded images
        :return: BytesIO with data of pdf file
        """
        slide_imgs = cls._base64_to_images(slides)

        out = BytesIO()
        first_slide_img: Image.Image = slide_imgs.__next__()
        first_slide_img.save(
            out, format="PDF", save_all=True, append_images=slide_imgs
        )
        out.seek(0)

        return out
