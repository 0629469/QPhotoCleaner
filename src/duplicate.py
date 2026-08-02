from collections import defaultdict


def find_duplicates(records):
    """
    records: list of dicts with keys 'path' and 'hash'
    returns duplicate groups
    """
    groups = defaultdict(list)

    for record in records:
        file_hash = record.get("hash")
        if file_hash:
            groups[file_hash].append(record)

    return [files for files in groups.values() if len(files) > 1]


def find_duplicates_from_rows(rows):
    """
    rows: [(path, hash), ...]
    """
    groups = defaultdict(list)

    for path, file_hash in rows:
        if file_hash:
            groups[file_hash].append(path)

    return [paths for paths in groups.values() if len(paths) > 1]
