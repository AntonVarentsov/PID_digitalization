from unittest import mock
from pidocr.database import insert_entities
from pidocr.extraction import ExtractedEntity


def test_insert_entities_calls_db():
    entity = ExtractedEntity(text="A1", left=0, top=0, width=1, height=1, conf=90, angle=0, entity_type="line_number")
    with mock.patch("pidocr.database.psycopg2.connect") as m_connect, \
         mock.patch("pidocr.database.get_database_url", return_value="postgresql://test"), \
         mock.patch("pidocr.database.execute_values") as m_exec:
        mock_conn = m_connect.return_value
        insert_entities("file.png", 1, [entity])
        assert m_connect.called
        m_exec.assert_called_once()
        mock_conn.cursor.assert_called()
