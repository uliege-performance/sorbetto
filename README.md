# sorbetto

Sorbetto: a Python Library to Produce Classification Tiles With Different Flavors

# dev instructions

## install and configure dev tools

```
cd {{path to root of sorbetto}}

pip install -e ".[dev]"

pre-commit install
```

When you commit, ruff will automatically verify that your code is properly
linted/formatted.

If there are any errors, they are corrected, BUT you have to re-add the fixed
files (`git status` to see which file are modified, `git add` to add them)

## generate documentation locally

Make sure you installed the necessary dependencies for the docs:

```
cd {{path to root of sorbetto}}

pip install -e ".[docs]"
```

The `-e` is not mandatory.

Then generate the html documentation:

```
cd {{path to root of sorbetto}}
cd docs
make html
```

The resulting documentation will be located at `docs/_build/html/index.html`.

It will be later possible to publish this documentation to `readthedocs.io`.
