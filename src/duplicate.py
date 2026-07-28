"""
QPhotoCleaner
Duplicate Engine
"""

from hashing import calculate_sha256


def calculate_hashes(db):

    rows = db.get_duplicate_size_candidates()

    print()
    print(f"SHA256対象 : {len(rows)}件")
    print()

    for row in rows:

        sha = calculate_sha256(row["path"])

        db.update_sha256(row["id"], sha)

    db.commit()