from .base import BaseTransformer
from .presentation import PresentationToPdf
from ..models.file import FileType


transformer_classes = {
    FileType.presentation: PresentationToPdf,
}
