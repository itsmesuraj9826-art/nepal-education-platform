"""
Run this once to fix the users table and insert provincial admins.
Usage:  python fix_db.py
"""
import os, sys
from dotenv import load_dotenv

load_dotenv()

import pymysql

conn = pymysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', '3306')),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', ''),
    database=os.getenv('DB_NAME', 'nepal_edu_platform'),
    charset='utf8mb4',
)

cursor = conn.cursor()

print("Step 1: Adding missing columns to users table...")
cursor.execute("""
    ALTER TABLE users
        ADD COLUMN IF NOT EXISTS province_id     INT NULL,
        ADD COLUMN IF NOT EXISTS district_id     INT NULL,
        ADD COLUMN IF NOT EXISTS municipality_id INT NULL,
        ADD COLUMN IF NOT EXISTS school_id       INT NULL
""")
conn.commit()
print("  OK")

print("Step 2: Inserting 7 provincial admin users...")
from werkzeug.security import generate_password_hash

admins = [
    (1, 'prov1_admin', 'prov1@edu.np', 'Koshi Province Admin',          'Province1@Nepal2026'),
    (2, 'prov2_admin', 'prov2@edu.np', 'Madhesh Province Admin',        'Province2@Nepal2026'),
    (3, 'prov3_admin', 'prov3@edu.np', 'Bagmati Province Admin',        'Province3@Nepal2026'),
    (4, 'prov4_admin', 'prov4@edu.np', 'Gandaki Province Admin',        'Province4@Nepal2026'),
    (5, 'prov5_admin', 'prov5@edu.np', 'Lumbini Province Admin',        'Province5@Nepal2026'),
    (6, 'prov6_admin', 'prov6@edu.np', 'Karnali Province Admin',        'Province6@Nepal2026'),
    (7, 'prov7_admin', 'prov7@edu.np', 'Sudurpashchim Province Admin',  'Province7@Nepal2026'),
]

for province_id, username, email, full_name, password in admins:
    pw_hash = generate_password_hash(password)
    cursor.execute("""
        INSERT INTO users (username, email, password_hash, full_name, role, province_id, is_active)
        VALUES (%s, %s, %s, %s, 'provincial', %s, 1)
        ON DUPLICATE KEY UPDATE
            password_hash = VALUES(password_hash),
            province_id   = VALUES(province_id),
            is_active     = 1
    """, (username, email, pw_hash, full_name, province_id))
    print(f"  {username} (Province {province_id}) — OK")

conn.commit()
cursor.close()
conn.close()

print("\nAll done! Provincial admin credentials:")
print("-" * 50)
for pid, uname, _, fname, pw in admins:
    print(f"  {uname:15s}  /  {pw}")
print("-" * 50)
print("Start the app:  python app.py")
