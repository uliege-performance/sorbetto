# sorbetto

Sorbetto: a Python Library for Producing Classification Tiles With Different Flavors

# dev instructions

## install and configure dev tools

```sh
cd {{path to root of sorbetto}}

pip install -e ".[dev]"

pre-commit install
```

When you commit, ruff will automatically verify that your code is properly
linted/formatted.

If there are any errors, they are corrected, BUT you have to re-add the fixed
files (`git status` to see which file are modified, `git add` to add them)

## generate documentation locally

Make sure you installed the necessary dependencies for the doc:

```sh
cd {{path to root of sorbetto}}

pip install -e ".[doc]"
```

The `-e` is not mandatory.

Then generate the html documentation:

```sh
cd {{path to root of sorbetto}}
cd doc

make html
```

The resulting documentation will be located at `doc/_build/html/index.html`.

It will be later possible to publish this documentation to `readthedocs.io`.

## build and publish package

Make sure you installed the necessary dependencies for the distribution:

```sh
cd {{path to root of sorbetto}}

pip install -e ".[dist]"
```

The `-e` is optional.

Then create the wheels:

```sh
cd {{path to root of sorbetto}}

python -m build
```

The build outputs will be located under `dist`. You can then upload them to the PyPI
test repository using the following step:

```sh
twine upload --repository testpypi dist/sorbetto-*
```

After checking that everything is as expected on the test repository, you can
upload to PyPI by removing the `--repository testpypi` option.
