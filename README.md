# sorbetto

Sorbetto: a Python Library to Produce Classification Tiles With Different Flavors

# dev instructions

## install ruff pre-commit

```
cd {{path to root of sorbetto}}

pip install -e ".[dev,docs]"

pre-commit install
```

When you commit, ruff will automatically verify that your code is properly linted/formatted.

You can omit the `docs` option if you do not want to build the documentation.

If there are any errors, they are corrected, BUT you have to re-add the fixed files (`git status` to see which file are modified, `git add` to add them)
