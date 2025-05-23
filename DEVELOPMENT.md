# flake8-bugbear development

So you want to help out? **Awesome**. Go you!

## Getting Started

We use GitHub. To get started I'd suggest visiting https://guides.github.com/

### Pre Install

Please make sure you system has the following:

- Python 3.8.0 or greater
- git cli client

Also ensure you can authenticate with GitHub via SSH Keys or HTTPS.

### Checkout `flake8-bugbear`

Lets now cd to where we want the code and clone the repo:

Remember to fork the repo for your PR via the UI or other means (cli).

- `cd somewhere`
- `git clone git@github.com:YOUR_USERNAME/flake8-bugbear.git`

### Development venv

One way to develop and install all the dependencies is to use a venv.

- Lets create one and upgrade `pip`

```console
python3 -m venv /path/to/venv
/path/to/venv/bin/pip install --upgrade pip setuptools wheel
```

- Then we install flake8-bugbear with the dev dependencies

```console
cd flake8-bugbear
/path/to/venv/bin/pip install -e '.[dev]'
```

## Writing Tests

flake8-bugbear has a test runner that will go through all files in `tests/eval_files/`, run them through the linter, and check that they emit the appropriate error messages.

The expected errors are specified by adding comments on the line where the error is expected, using the format `# <error_code>: <col_offset>[, <var1>][, <var2>][...]`. E.g.
```python
x = ++n  # B002: 4
try:
    ...
except* (ValueError,):  # B013: 0, "ValueError", "*"
    ...
```
The error code should be in the `error_codes` dict, and the other values are passed to `eval` so should be valid python objects.

You can also specify options to be passed to `BugBearChecker` with an `# OPTIONS` comments
```python
# OPTIONS: extend_immutable_calls=["fastapi.Depends", "fastapi.Query"]
# OPTIONS: classmethod_decorators=["mylibrary.makeclassmethod", "validator"], select=["B902"]
```

If you specify a python version somewhere in the file name with `_pyXX`, the file will be skipped on smaller versions. Otherwise the name has no impact on the test, and you can test multiple errors in the same file.

The infrastructure is based on the test runner in https://github.com/python-trio/flake8-async which has some additional features that can be pulled into flake8-bugbear when desired.


## Running Tests

flake8-bugbear uses coverage to run standard unittest tests.

```console
/path/to/venv/bin/coverage run -m pytest tests/test_bugbear.py
```

You can also use [tox](https://tox.wiki/en/latest/index.html) to test with multiple different python versions, emulating what the CI does.

```console
/path/to/venv/bin/tox
```
will by default run all tests on python versions 3.9 through 3.13. If you only want to test a specific version you can specify the environment with `-e`

```console
/path/to/venv/bin/tox -e py313
```

## Running linter

We format the code with `black` and `isort`. You can run those using `pre-commit`.

```console
pre-commit run --all-files
```

Or you install the pre-commit hooks to run on every commit:

```console
pre-commit install
```
