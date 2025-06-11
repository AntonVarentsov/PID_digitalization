"""Entity extraction utilities."""
from dataclasses import dataclass
import re
from typing import Iterable, List
from .ocr import OCRResult

LINE_PATTERN = re.compile(r"\b[A-Z]{1,2}\d{2,}\b")
EQUIPMENT_PATTERN = re.compile(r"\b[A-Z]{1,3}-\d{3,}\b")


@dataclass
class ExtractedEntity(OCRResult):
    """OCR result with classified entity."""
    entity_type: str


def extract_entities(results: Iterable[OCRResult]) -> List[ExtractedEntity]:
    """Extract equipment tags and line numbers from OCR results."""
    entities: List[ExtractedEntity] = []
    for res in results:
        if LINE_PATTERN.search(res.text):
            etype = "line_number"
        elif EQUIPMENT_PATTERN.search(res.text):
            etype = "equipment_tag"
        else:
            continue
        entity = ExtractedEntity(
            text=res.text,
            left=res.left,
            top=res.top,
            width=res.width,
            height=res.height,
            conf=res.conf,
            angle=res.angle,
            entity_type=etype,
        )
        entities.append(entity)
    return entities
