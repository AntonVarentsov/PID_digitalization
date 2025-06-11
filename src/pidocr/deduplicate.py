"""Deduplication utilities for OCR results."""
from typing import List
from .ocr import OCRResult


def deduplicate_results(results: List[OCRResult], iou_threshold: float = 0.5) -> List[OCRResult]:
    """Remove near-duplicate OCR results based on overlap and text match."""
    deduped: List[OCRResult] = []
    for res in results:
        duplicate = False
        for other in deduped:
            if res.text == other.text and _iou(res, other) > iou_threshold:
                duplicate = True
                break
        if not duplicate:
            deduped.append(res)
    return deduped


def _iou(a: OCRResult, b: OCRResult) -> float:
    """Compute intersection-over-union of two boxes."""
    x1 = max(a.left, b.left)
    y1 = max(a.top, b.top)
    x2 = min(a.left + a.width, b.left + b.width)
    y2 = min(a.top + a.height, b.top + b.height)
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    area_a = a.width * a.height
    area_b = b.width * b.height
    union = area_a + area_b - inter_area
    return inter_area / union if union else 0.0
