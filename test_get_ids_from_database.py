from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from get_ids_database import get_ids_from_database

load_dotenv()


def test_get_ids_from_database():
    # Create a test database
    engine = create_engine(os.getenv('ENGINE'))

    # Create a test table and insert some data
    with engine.connect() as conn:
        try:
            conn.execute(text("CREATE TABLE test_table (id int, name text)"))

            conn.execute(
                text("INSERT INTO test_table (id, name) VALUES (:id, :name)"),
                [
                    {"id": 1, "name": "Vicky"},
                    {"id": 2, "name": "Juaner"},
                    {"id": 3, "name": "Chang"}
                ]
            )

            conn.commit()
        # If the table already exists in the database, the except block does
        # nothing and allowing the script to continue executing without raising
        # an error.
        except Exception:
            pass

    # Test the function with a sample SQL query
    query = 'SELECT id FROM test_table WHERE name LIKE \'V%\''
    expected_result = [1]

    result = get_ids_from_database(query, engine)
    assert result == expected_result
