from database.connection import get_connection
from database.models import (
    FILES_TABLE,
    PYTHON_CLASSES_TABLE,
    PYTHON_FUNCTIONS_TABLE,
    PYTHON_IMPORTS_TABLE,
)


def initialize_database() -> None:
    """
    Create all required tables.
    """

    with get_connection() as conn:

        cursor = conn.cursor()

        cursor.execute(FILES_TABLE)
        cursor.execute(PYTHON_IMPORTS_TABLE)
        cursor.execute(PYTHON_FUNCTIONS_TABLE)
        cursor.execute(PYTHON_CLASSES_TABLE)

        conn.commit()