![sorbetto banner](doc/src/images/sorbetto_banner.svg)

# Sorbetto

Sorbetto: a Python Library for Producing Classification Tiles With Different Flavors

# dev instructions

## install and configure dev tools

```bash
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

```bash
cd {{path to root of sorbetto}}

pip install -e ".[doc]"
```

The `-e` is not mandatory.

You also need to install `pandoc` to properly export the example notebooks.
Follow the instructions on the [pandoc documentation](https://pandoc.org/installing.html).

Then generate the html documentation:

```bash
cd {{path to root of sorbetto}}
cd doc

make html
```

The resulting documentation will be located at `doc/_build/html/index.html`.

It will be later possible to publish this documentation to `readthedocs.io`.

## include figures in the documentation

It is possible to include figures and images in the documentation by using the
following syntax:

```rst
.. image:: /figures/{{path_to_your_figure}}
```

Most common image formats should work, `svg` is recommended for size and
resolution.

If you want to add existing images to the documentation, please add them to the
`images` folder (and replace `figures` by `images` in the rst directive).

If you want to generate new figures programmatically, you can create new scripts
in `doc/scripts`. You should include `doc/scripts/utils` and use the helper
function `run_and_save` to call your plotting function. It will save the figure
in the right location, and avoid running unnecessary code if the figure already
exists (to re-generate a figure, please delete it first).

Then, run the following to execute all the figure scripts:

```bash
cd {{path to root of sorbetto}}
cd doc

make figures
```

## build and publish package

Make sure you installed the necessary dependencies for the distribution:

```bash
cd {{path to root of sorbetto}}

pip install -e ".[dist]"
```

The `-e` is optional.

Then create the wheels:

```bash
cd {{path to root of sorbetto}}

python -m build
```

The build outputs will be located under `dist`. You can then upload them to the PyPI
test repository using the following step:

```bash
twine upload --repository testpypi dist/sorbetto-*
```

After checking that everything is as expected on the test repository, you can
upload to PyPI by removing the `--repository testpypi` option.
