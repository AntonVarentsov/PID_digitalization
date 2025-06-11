"""Command line interface for PID OCR processing."""
import argparse
import logging
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image

from .preprocessing import load_image, preprocess_image
from .ocr import ocr_image
from .extraction import extract_entities
from .deduplicate import deduplicate_results
from .database import init_db, insert_entities
from .exporter import export_to_csv, export_to_excel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_file(path: Path, page: int = 1, export: Path | None = None) -> None:
    """Process a single image or PDF file."""
    if path.suffix.lower() == ".pdf":
        images = convert_from_path(path)
    else:
        images = [load_image(path)]

    for page_num, img in enumerate(images, start=page):
        processed = preprocess_image(img)
        ocr_results = ocr_image(processed)
        deduped = deduplicate_results(ocr_results)
        entities = extract_entities(deduped)
        insert_entities(path.name, page_num, entities)
        if export:
            export_to_csv(path.name, page_num, entities, str(export.with_suffix(".csv")))
            export_to_excel(path.name, page_num, entities, str(export.with_suffix(".xlsx")))


def main() -> None:
    parser = argparse.ArgumentParser(description="Process PID images for OCR")
    parser.add_argument("input", type=Path, help="Input file or directory")
    parser.add_argument("--export", type=Path, help="Optional path prefix for CSV/Excel export")
    args = parser.parse_args()

    init_db()

    if args.input.is_dir():
        for file in args.input.iterdir():
            if file.suffix.lower() in {".pdf", ".png", ".jpg", ".jpeg", ".tiff"}:
                logger.info("Processing %s", file)
                process_file(file, export=args.export)
    else:
        process_file(args.input, export=args.export)


if __name__ == "__main__":
    main()
