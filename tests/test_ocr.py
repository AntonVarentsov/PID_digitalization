from PIL import Image, ImageDraw
import pytest
import pytesseract

from pidocr.ocr import ocr_image


def test_ocr_image(tmp_path):
    try:
        pytesseract.get_tesseract_version()
    except pytesseract.TesseractNotFoundError:
        pytest.skip("tesseract not installed")
    img = Image.new("RGB", (200, 100), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((10, 40), "A1-001", fill="black")
    results = ocr_image(img, angles=[0])
    texts = [r.text for r in results]
    assert any("A1-001" in t for t in texts)
