from PIL import Image
from pidocr.preprocessing import preprocess_image

def test_preprocess_image(tmp_path):
    img_path = tmp_path / "test.png"
    Image.new("RGB", (100, 100), color="white").save(img_path)
    img = Image.open(img_path)
    processed = preprocess_image(img)
    assert processed.mode == "L"
    assert processed.size == img.size
