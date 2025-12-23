
# Reproducible Example – `Resource.path` as `list[str]`

This repository is a **minimal reproducible example (reprex)** created to illustrate the **Frictionless specification**, which allows [`Resource.path` to be a `list[str]`](https://datapackage.org/standard/data-resource/#multiple-files) for multi-file resources and that the **Python API ([`frictionless-py`](https://pypi.org/project/frictionless/))**, validates `datapackage.json`.

### Why this repo exists

To help the problem described in [this Issue](https://github.com/frictionlessdata/frictionless-py/issues/1761).

This reprex has a simple structure:

```bash
.
├── datapackage.json
├── data
│   ├── example1.csv
│   └── example2.csv
└── README.md
```

As we could see, running validation via the CLI works correctly when `path` is a list:

```bash
(venv) ➜  open-reprex git:(frictionless_resource_path_as_list) ✗ frictionless validate datapackage.json
────────────────────────────────────────────────────────────────────────── Dataset ───────────────────────────────────────────────────────────────────────────
                               dataset
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ name             ┃ type  ┃ path                          ┃ status ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ example-resource │ table │ data/example1.csv (multipart) │ VALID  │
└──────────────────┴───────┴───────────────────────────────┴────────┘
```

## Setup

Clone the branch used for this reproducible example:

```bash
git clone --branch 20251223_frictionless_resource_path_as_list --single-branch git@github.com:gabrielbdornas/reprex.git
cd reprex
```

### Option A — Using Poetry (recommended)

This project is managed with **Poetry**.

```bash
poetry install
```

### Option B — Using `pip` + `venv`

If you prefer not to use Poetry, you can install the frictionless using `pip`.

```bash
python3 -m venv venv
source venv/bin/activate
pip install frictionless==5.18.1
```

## Validation test (works as expected)

From the project root, run:

```bash
# Using Poetry
poetry run frictionless validate datapackage.json

# Using pip
# need virtual env active
frictionless validate datapackage.json
```

Expected result:

* Validation succeeds.
* The resource loads both CSV files listed in `path`.
* Confirms that `path` as `list[str]` works when defined in a Datapackage resource.
