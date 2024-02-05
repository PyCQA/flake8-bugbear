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

## Running Tests

flake8-bugbear uses coverage to run standard unittest tests.

```console
/path/to/venv/bin/coverage run tests/test_bugbear.py
```

You can also use [tox](https://tox.wiki/en/latest/index.html) to test with multiple different python versions, emulating what the CI does.

```console
/path/to/venv/bin/tox
```
will by default run all tests on python versions 3.8 through 3.12. If you only want to test a specific version you can specify the environment with `-e`

```console
/path/to/venv/bin/tox -e py38
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
