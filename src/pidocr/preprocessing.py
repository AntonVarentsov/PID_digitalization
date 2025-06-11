"""Image loading and preprocessing utilities."""
from pathlib import Path
from typing import Union
from PIL import Image, ImageFilter
import cv2
import numpy as np


def load_image(path: Union[str, Path]) -> Image.Image:
    """Load an image from disk."""
    return Image.open(path)


def preprocess_image(image: Image.Image) -> Image.Image:
    """Convert image to grayscale and apply thresholding and denoising."""
    gray = image.convert("L")
    img_array = np.array(gray)
    _, thresh = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised = cv2.medianBlur(thresh, 3)
    result = Image.fromarray(denoised).filter(ImageFilter.SHARPEN)
    return result
