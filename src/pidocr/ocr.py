"""OCR utilities with multi-angle support."""
from dataclasses import dataclass
from typing import List
from PIL import Image
import pytesseract


@dataclass
class OCRResult:
    """Data for a single OCR result."""
    text: str
    left: int
    top: int
    width: int
    height: int
    conf: int
    angle: int


def _rotate_image(image: Image.Image, angle: int) -> Image.Image:
    """Rotate image by angle degrees."""
    return image.rotate(angle, expand=True)


def _transform_bbox(bbox: tuple, angle: int, orig_size: tuple) -> tuple:
    """Transform bounding box from rotated image to original coordinates."""
    x, y, w, h = bbox
    if angle == 0:
        return bbox
    img_w, img_h = orig_size
    if angle == 90:
        return (img_h - y - h, x, h, w)
    if angle == 180:
        return (img_w - x - w, img_h - y - h, w, h)
    if angle == 270:
        return (y, img_w - x - w, h, w)
    return bbox


def ocr_image(image: Image.Image, angles: List[int] | None = None) -> List[OCRResult]:
    """Run OCR on image for multiple angles."""
    if angles is None:
        angles = [0, 90, 180, 270]
    results: List[OCRResult] = []
    for angle in angles:
        rotated = _rotate_image(image, angle)
        data = pytesseract.image_to_data(rotated, output_type=pytesseract.Output.DICT)
        n_boxes = len(data['text'])
        for i in range(n_boxes):
            text = data['text'][i].strip()
            if text:
                bbox = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                bbox = _transform_bbox(bbox, angle, image.size)
                result = OCRResult(
                    text=text,
                    left=bbox[0],
                    top=bbox[1],
                    width=bbox[2],
                    height=bbox[3],
                    conf=int(float(data['conf'][i])),
                    angle=angle,
                )
                results.append(result)
    return results
