"""PostgreSQL interaction utilities."""
from typing import Iterable
import logging
import psycopg2
from psycopg2.extras import execute_values

from .config import get_database_url
from .extraction import ExtractedEntity

logger = logging.getLogger(__name__)

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS pid_entities (
    id SERIAL PRIMARY KEY,
    filename TEXT,
    page INTEGER,
    tag_type TEXT,
    tag_text TEXT,
    left INTEGER,
    top INTEGER,
    width INTEGER,
    height INTEGER,
    confidence INTEGER,
    angle INTEGER
);
"""

INSERT_SQL = """
INSERT INTO pid_entities
(filename, page, tag_type, tag_text, left, top, width, height, confidence, angle)
VALUES %s
"""


def init_db() -> None:
    """Initialize database and create table if needed."""
    conn = psycopg2.connect(get_database_url())
    with conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)
    conn.close()


def insert_entities(filename: str, page: int, entities: Iterable[ExtractedEntity]) -> None:
    """Insert extracted entities into database."""
    conn = psycopg2.connect(get_database_url())
    records = [
        (
            filename,
            page,
            ent.entity_type,
            ent.text,
            ent.left,
            ent.top,
            ent.width,
            ent.height,
            ent.conf,
            ent.angle,
        )
        for ent in entities
    ]
    with conn:
        with conn.cursor() as cur:
            execute_values(cur, INSERT_SQL, records)
    conn.close()
