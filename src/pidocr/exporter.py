"""Export utilities for PID OCR results."""
from typing import Iterable
import pandas as pd
from .extraction import ExtractedEntity


def _to_records(filename: str, page: int, entities: Iterable[ExtractedEntity]):
    for ent in entities:
        yield {
            "filename": filename,
            "page": page,
            "tag_type": ent.entity_type,
            "tag_text": ent.text,
            "left": ent.left,
            "top": ent.top,
            "width": ent.width,
            "height": ent.height,
            "confidence": ent.conf,
            "angle": ent.angle,
        }


def export_to_csv(filename: str, page: int, entities: Iterable[ExtractedEntity], output_path: str) -> None:
    """Export entities to CSV file."""
    pd.DataFrame(list(_to_records(filename, page, entities))).to_csv(output_path, index=False)


def export_to_excel(filename: str, page: int, entities: Iterable[ExtractedEntity], output_path: str) -> None:
    """Export entities to Excel file."""
    pd.DataFrame(list(_to_records(filename, page, entities))).to_excel(output_path, index=False)
