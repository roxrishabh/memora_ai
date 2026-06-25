FILES_TABLE = """
CREATE TABLE IF NOT EXISTS files (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    path TEXT NOT NULL UNIQUE,

    filename TEXT NOT NULL,

    extension TEXT NOT NULL,

    file_type TEXT,

    programming_language TEXT,

    mime_type TEXT,

    size INTEGER,

    created_at TEXT,

    modified_at TEXT,

    sha256 TEXT,

    indexed_at TEXT
);
"""

PYTHON_IMPORTS_TABLE = """
CREATE TABLE IF NOT EXISTS python_imports (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    file_id INTEGER NOT NULL,

    module TEXT NOT NULL,

    FOREIGN KEY(file_id)
        REFERENCES files(id)
        ON DELETE CASCADE
);
"""

PYTHON_FUNCTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS python_functions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    file_id INTEGER NOT NULL,

    function_name TEXT NOT NULL,

    FOREIGN KEY(file_id)
        REFERENCES files(id)
        ON DELETE CASCADE
);
"""

PYTHON_CLASSES_TABLE = """
CREATE TABLE IF NOT EXISTS python_classes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    file_id INTEGER NOT NULL,

    class_name TEXT NOT NULL,

    FOREIGN KEY(file_id)
        REFERENCES files(id)
        ON DELETE CASCADE
);
"""