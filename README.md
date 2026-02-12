# argparse examples — reproduction of the howto guide

This repository contains small example scripts reproduced from the Python
`argparse` how-to documentation. Each script demonstrates a specific usage
pattern or feature of the `argparse` library (positional arguments, optional
arguments, `store_true` actions, type conversion, mutually exclusive groups,
etc.).

**What I did**
- Recreated the examples from the `argparse` [how-to guide as standalone](https://docs.python.org/3/howto/argparse.html#custom-type-converters)
  Python scripts, so each concept is easy to run and inspect.

**Files**
- `001_the_basics.py`: minimal `ArgumentParser()` and `parse_args()` usage.
- `002_positional_arguments.py`: a simple positional argument and printing it.
- `003_positional_arguments_cast_int.py`: positional argument with `type=int`.
- `004_optional_arguments.py`: optional flag with a value (string by default).
- `005_optional_arguments_story_true.py`: optional flag using `action='store_true'`.
- `006_mix_positional_and_optional_arguments.py`: mixing a typed positional
  argument with a `store_true` verbose flag.
- `007_mix_positional_and_optional_arguments_without_store_true.py`: numeric
  verbosity using `choices` and branching behavior.
- `008_mix_positional_and_optional_arguments_without_store_true.py`: same idea
  but with a `default` verbosity level and thresholded checks.
- `009_mix_positional_and_optional_arguments.py`: two positional args (base,
  exponent) and numeric verbosity levels.
- `010_mutually_exclusive_group.py`: example of `add_mutually_exclusive_group()`
  to ensure `--verbose` and `--quiet` cannot both be given.

**Quick argparse review**
- **Purpose**: `argparse` parses command-line arguments and produces a
  namespace object with attributes for each argument.
- **Core classes/functions**: `ArgumentParser`, `add_argument(...)`,
  and `parse_args()`.
- **Positional vs optional**: positional args are required by position; optional
  args use `-` or `--` flags and can have short/long forms.
- **Types & conversions**: use `type=` to convert incoming string values
  (e.g. `type=int`). For complex validation, pass a callable to `type` that
  raises `ArgumentTypeError` on invalid values.
- **Actions**: `action='store_true'` / `store_false` for boolean flags,
  `append` to collect multiple values, and others for common behaviors.
- **Choices & defaults**: `choices=` restricts allowed values; `default=`
  supplies a default when the option is omitted.
- **Mutually exclusive groups**: `add_mutually_exclusive_group()` prevents
  conflicting options from being given together.
- **Help & usage**: `ArgumentParser` auto-generates `-h/--help` and usage
  strings; provide clear `help=` texts for good UX.
- **Custom type converters**: pass a function to `type=` to implement parsing
  and validation (this is what the how-to section you read focuses on).
- **Good practices**: use explicit flags, validate values early, prefer
  descriptive `help` strings, consider `subparsers` for multi-command CLIs,
  and keep argument parsing logic separate from business logic for testability.

**Run the examples**
Try them directly from the repository root. Examples:

```bash
python 001_the_basics.py
python 002_positional_arguments.py hello
python 003_positional_arguments_cast_int.py 5
python 006_mix_positional_and_optional_arguments.py 4 -v
python 009_mix_positional_and_optional_arguments.py 2 8 -v 2
```
