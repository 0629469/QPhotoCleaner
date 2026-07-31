"""
QPhotoCleaner Duplicate Engine
"""
from hashing import calculate_sha256

class DuplicateEngine:
    def __init__(self, db):
        self.db=db
    def calculate_hashes(self):
        rows=self.db.get_duplicate_size_candidates()
        total=len(rows)
        print(f"SHA-256計算対象:{total}件")
        for i,row in enumerate(rows,1):
            self.db.update_sha256(row["id"], calculate_sha256(row["path"]))
            if i%50==0 or i==total:
                print(f"{i}/{total}")
        self.db.commit()
        if hasattr(self.db,"mark_duplicates"):
            self.db.mark_duplicates()
    def show_duplicates(self):
        rows=self.db.get_duplicate_hashes()
        g=None;c=0
        for r in rows:
            grp=r["duplicate"] if "duplicate" in r.keys() else r["sha256"]
            if grp!=g:
                g=grp
                print(f"\n===== Group {grp} =====")
            print(r["path"]);c+=1
        return c
