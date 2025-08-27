# sorbetto
Sorbetto: a Python Library to Produce Classification Tiles With Different Flavors


# dev instructions

## install ruff pre-commit

```
cd {{path to root of sorbetto}}

pip install ruff pre-commit

pre-commit install
```

When you commit, ruff will automatically verify that your code is properly linted/formatted. 

If there are any errors, they are corrected, BUT you have to re-add the fixed files (`gti status` to see which file are modified, `git add` to add them)
