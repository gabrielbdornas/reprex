"""Data loader: builds a compact filter index linking fact_credito to linktable.

For every key_credito found in fact_credito.csv.gz, scans linktable.csv.gz and
records which values each dimension column takes on for that key (the "facets").
Also records the global set of selectable values per column (the "options").

This avoids shipping the full linktable (856k rows) or a flat exploded join
(615k+ rows, since fact_credito's dimensions are coarser than other resources')
to the browser. The output stays bounded by fact_credito's own row count.

Runs at build/preview time (Observable Framework data loader convention).
Writes JSON to stdout. Uses only the standard library.
"""
import csv
import gzip
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "datapackages" / "siafi" / "data" / "linktable"

JOIN_KEY = "key_credito"


def read_csv_gz(path):
    with gzip.open(path, "rt", newline="") as f:
        yield from csv.reader(f)


def main():
    fact_rows = read_csv_gz(DATA_DIR / "fact_credito.csv.gz")
    fact_header = next(fact_rows)
    fact_key_idx = fact_header.index(JOIN_KEY)
    credito_keys = {row[fact_key_idx] for row in fact_rows}

    link_rows = read_csv_gz(DATA_DIR / "linktable.csv.gz")
    link_header = next(link_rows)
    link_key_idx = link_header.index(JOIN_KEY)
    dimension_idxs = [
        i for i, name in enumerate(link_header)
        if not name.startswith("key") and i != link_key_idx
    ]
    dimension_names = [link_header[i] for i in dimension_idxs]

    facets = {key: {} for key in credito_keys}
    options = {name: set() for name in dimension_names}

    for row in link_rows:
        key = row[link_key_idx]
        if key not in facets:
            continue
        row_facets = facets[key]
        for i, name in zip(dimension_idxs, dimension_names):
            value = row[i]
            if not value:
                continue
            row_facets.setdefault(name, set()).add(value)
            options[name].add(value)

    output = {
        "columns": dimension_names,
        "options": {name: sorted(values) for name, values in options.items()},
        "facets": {
            key: {name: sorted(values) for name, values in cols.items()}
            for key, cols in facets.items()
        },
    }
    json.dump(output, sys.stdout, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main()
