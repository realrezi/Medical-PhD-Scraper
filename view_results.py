import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load Neon connection string from environment variable
NEON_URL = os.environ.get("NEON_URL")

if not NEON_URL:
    raise ValueError(
        "NEON_URL environment variable is not set. Please set it in your .env file.")


def view_recent_matches(limit=10):
    print(
        f"Connecting to Neon database to fetch the latest {limit} matches...\n")
    try:
        conn = psycopg2.connect(NEON_URL)
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'medical_vacancies'
            );
        """)
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            print("No database table found. Please run the scraper first.")
            return

        cursor.execute(
            "SELECT id, title, url FROM medical_vacancies ORDER BY id DESC LIMIT %s;", (limit,))
        rows = cursor.fetchall()

        if not rows:
            print("No medical PhD positions found in the database yet.")
        else:
            print("=" * 60)
            print(f"🏥 MOST RECENT MEDICAL PHD POSITIONS ({len(rows)})")
            print("=" * 60 + "\n")

            for row in rows:
                job_id, title, url = row
                print(f"🎓 {title}")
                print(f"🔗 {url}")
                print("-" * 60)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error accessing database: {e}")


if __name__ == "__main__":
    import sys
    limit = 10
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        limit = int(sys.argv[1])

    view_recent_matches(limit)
