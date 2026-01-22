# Reproducible Example – `fieldsMatch`

This repository is a **minimal reproducible example (reprex)** created to test the [`fieldsMatch`](https://datapackage.org/standard/table-schema/#fieldsMatch) property at the Table Schema level in **Frictionless specification**.

### Why this repo exists

To help the problem described in [this Issue](https://github.com/frictionlessdata/frictionless-py/issues/1763).

This reprex has a simple structure[^1]:

[^1]: `tree --gitignore`

```bash
.
├── data
│   ├── data_1_field.csv
│   ├── data_2_fields.csv
│   ├── data_full.csv
│   └── data_without_fields.csv
├── datapackage.json
├── README.md
├── requirements.txt
└── schemas
    ├── dialect.json
    └── schema.json
```

## Setup

Clone the branch used for this reproducible example:

```bash
git clone --branch 20260122_frictionless-fieldsMatch-test --single-branch git@github.com:gabrielbdornas/reprex.git
cd reprex

# Python Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Validation test CLI (works as expected)

From the project root, run:

```bash
# Using pip
# need virtual env active
frictionless validate datapackage.json
```
