"""Data loader: passthrough of fact_credito.csv.gz, decompressed, as-is.

Runs at build/preview time (Observable Framework data loader convention).
Writes CSV to stdout. Uses only the standard library.
"""
import gzip
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FACT_PATH = REPO_ROOT / "datapackages" / "siafi" / "data" / "linktable" / "fact_credito.csv.gz"


def main():
    with gzip.open(FACT_PATH, "rt", newline="") as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()
