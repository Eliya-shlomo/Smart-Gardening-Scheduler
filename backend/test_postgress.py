from database import get_db
from sqlalchemy import text
from sqlalchemy.exc import OperationalError


def test_connection():
    try:
        db = next(get_db())

        result = db.execute(text("SELECT 1"))

        print("✅ Success! Connected to the database.")
        print("Returned:", result.scalar())

    except OperationalError as e:
        print("❌ Failed to connect to the database.")
        print("Error:", e)

    except Exception as e:
        print("❌ An unexpected error occurred.")
        print("Error:", e)


if __name__ == "__main__":
    test_connection()
