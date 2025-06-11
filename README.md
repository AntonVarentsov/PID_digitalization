# PID Digitalization

This project provides tools to extract pipeline and equipment tag information from
P\&ID diagrams (PDF or image files) using OCR. Recognized tags are stored in a
PostgreSQL database for further processing and review.

## Features

- Image pre-processing (grayscale, threshold, denoise)
- Multi-angle OCR (0\°, 90\°, 180\°, 270\°) with bounding box correction
- Extraction of line numbers and equipment tags via regular expressions
- Deduplication of OCR results across rotations
- Results stored in PostgreSQL using settings from `.env`
- Optional export to CSV or Excel
- Modular structure prepared for future visualization or UI extensions

## Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and update the `DATABASE_URL` to point to your
   PostgreSQL instance.

3. Ensure Tesseract OCR and poppler utilities are installed on your system
   (required by `pytesseract` and `pdf2image`).

## Usage

Process a folder of images or a single file:

```bash
python -m pidocr.main /path/to/folder --export results/output
```

OCR results will be inserted into the configured database. If `--export` is
provided, CSV and Excel files will also be generated for each processed file.

## Database Schema

The application creates a table named `pid_entities` with the following columns:

- `id` – serial primary key
- `filename` – original file name
- `page` – page number within the file
- `tag_type` – `line_number` or `equipment_tag`
- `tag_text` – recognized text
- `left`, `top`, `width`, `height` – bounding box in pixels
- `confidence` – OCR confidence value
- `angle` – rotation angle used during OCR

## Running Tests

Unit tests are located in the `tests/` directory and can be executed with
`pytest`:

```bash
pytest
```

## Project Goals

The codebase is structured to allow future extensions such as deep learning
models for improved OCR, interactive UIs for reviewing results, and web or
desktop applications for visualization.
