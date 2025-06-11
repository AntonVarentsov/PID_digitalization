from pidocr.ocr import OCRResult
from pidocr.deduplicate import deduplicate_results


def test_deduplicate_results():
    r1 = OCRResult(text="A1", left=10, top=10, width=50, height=20, conf=90, angle=0)
    r2 = OCRResult(text="A1", left=12, top=12, width=50, height=20, conf=88, angle=90)
    deduped = deduplicate_results([r1, r2])
    assert len(deduped) == 1
