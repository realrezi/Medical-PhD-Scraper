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


def save_to_neon(valid_positions):
    print("Connecting to Neon database...")

    # 1. Connect to the Neon database
    conn = psycopg2.connect(NEON_URL)
    cursor = conn.cursor()

    # 2. Create the table if it doesn't exist yet
    # We set URL as UNIQUE so you never save duplicate jobs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medical_vacancies (
            id SERIAL PRIMARY KEY,
            title TEXT,
            url TEXT UNIQUE,
            description TEXT
        );
    ''')

    # 3. Insert the new jobs
    inserted_count = 0
    for job in valid_positions:
        try:
            # ON CONFLICT DO NOTHING ensures we ignore a job if it's already in the database
            cursor.execute('''
                INSERT INTO medical_vacancies (title, url, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
            ''', (job['title'], job['url'], job.get('description', '')))

            # If a new row was actually added, count it
            if cursor.rowcount > 0:
                inserted_count += 1
        except Exception as e:
            print(f"Database error for {job['url']}: {e}")

    # 4. Save and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    print(
        f"☁️ Successfully saved {inserted_count} new vacancies to your Neon cloud database!")
