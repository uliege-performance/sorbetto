.. _Contributing:

Contributing
============

If you wish to help us extend and improve Sorbetto, you are in the right place!
This guide will give you all the information to get started and contribute to
our library. Please read it carefully before submitting your contribution, as it
will facilitate integrating it into the library if it is compliant with our
guidelines.

If you are ready to submit your contribution (great, thanks!), please create a
new `pull request <https://github.com/uliege-performance/sorbetto/pulls>`__, and
we will get in touch with you as soon as possible.


.. contents:: Table of Contents
    :backlinks: none
    :depth: 4


Setting up the development environment
--------------------------------------

First, we highly recommend that you use a virtual environment for development.
In that environment, install Sorbetto with its dev dependencies and configure
the pre-commit hooks:

.. code-block:: bash

    git clone https://github.com/uliege-performance/sorbetto.git
    cd sorbetto
    pip install -e ".[dev]"
    pre-commit install

The pre-commit hooks will ensure that your code is compliant with our automatic
requirements checked by the GitHub actions. These include formatting, linting,
and license headers.

If you attempt to commit non-compliant code, the pre-commit hooks will warn you
and fix the issues automatically if possible. After the fix, simply add the
modified files and commit again. 

If you push non-compliant commits, the GitHub actions will flag them and prevent
merging any pull requests until the issues are fixed. You will receive an email
notification with the details of the errors.

If you are using VS Code, you can install the `Ruff
<https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff>`__
extension and configure it to format your code (and sort imports) automatically.
This will ensure that you are compliant with the pre-commit format requirements.


Coding guidelines
-----------------

In order to keep the codebase consistent and clear, please follow these
guidelines when contributing code:


Formatting
^^^^^^^^^^

We use Ruff to automatically format the code. We recommend that you enable the
pre-commit hooks (see `Setting up the development environment`_) to ensure that
your code is correctly formatted before committing. Compliance with this
formatting is also enforced by GitHub actions.


Licensing
^^^^^^^^^

All code files must include the Sorbetto license header at the top of the file.
The header is as follows::

    Copyright (c) {year_start}-{year_end}, Sebastien Pierard et al.
    SPDX-License-Identifier: Apache-2.0

If you configured the pre-commit hooks (see `Setting up the development
environment`_), the license header will be automatically updated in any committed
files. Compliance with this requirement is also enforced by GitHub actions.


Using git
^^^^^^^^^

We use git for version control. Pushing directly to the main repository is not
allowed.  Instead, we you must create a branch for any new feature or bug
fix, and then submit a `pull request
<https://github.com/uliege-performance/sorbetto/pulls>`__ when the work is
complete.

When creating a branch, please base it on the latest version of the ``dev``
branch.  The ``dev`` branch contains the latest development changes, while the
``main`` gets updated only for releases or major fixes. Use a descriptive name
for your branch.

Before submitting a pull request to the ``dev`` branch, please sync your branch
with the latest changes from ``dev``. Preferably, use rebasing instead of
merging to keep a clean history when appropriate. See this `tutorial by
Atlassian <https://www.atlassian.com/git/tutorials/merging-vs-rebasing>`__ to
understand the difference between the two, and in which situations each option
is preferable.


Documentation
-------------

This section provides guidelines on how to contribute to the documentation, and
instructions to build the documentation locally.

The documentation is located in two places:

* ``sorbetto/doc/src``: the rst files that make the structure of the
  documentation.
* ``sorbetto/sorbetto``: the API reference is automatically compiled from the
  docstrings present in the code. **It is therefore mandatory to correctly
  document all additions to the codebase.**


Writing docstrings
^^^^^^^^^^^^^^^^^^

All modules, classes, methods, and functions must be correctly documented in
order to populate the API reference. We use the Google style docstring format:

.. code-block:: python

    def abc(a: int, c = [1,2]):
        """_summary_

        Args:
            a (int): _description_
            c (list, optional): _description_. Defaults to [1,2].

        Raises:
            AssertionError: _description_

        Returns:
            _type_: _description_
        """
        if a > 10:
            raise AssertionError("a is more than 10")

        return c

If you are using VS Code, you can set up the `autoDocstring
<https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring>`__
extension to automatically generate templates for you.

In order to be as precise as possible, we encourage the use of type hints
everywhere.


Writing math
""""""""""""

You can include math in your docstrings, the Latex way! **All backslashes
must be doubled to avoid failures** (only in docstrings, not rst files).

You can use inline math (equivalent to single $):

.. code-block:: rst

    :math:`\\tau = \\left\\{ \\frac{\\pi}{42} \\right\\}`

Or have your equations on a separate line (equivalent to double $$):

.. code-block:: rst

    .. math::

        \\tau = \\left\\{ \\frac{\\pi}{42} \\right\\}

These will be rendered as: 

.. math::
    \tau = \left\{ \frac{\pi}{42} \right\}

In jupyter notebooks, you can use standard $ and $$ in markdown cells.


Citing references
"""""""""""""""""

We use a bibtex file to list all the references used throughout the documentation.
You can cite references in the documentation (and docstrings) as follows:

.. code-block:: rst

    :cite:t:`<bibtex key>`
    :cite:p:`<bibtex key>`

The ``:cite:t:`` directive generates a textual citation (e.g.
:cite:t:`Pierard2024TheTile-arxiv`), while ``:cite:p:`` generates a parenthetical
citation (e.g. :cite:p:`Pierard2024TheTile-arxiv`).

All the references are listed in the ``sorbetto/doc/references.bib`` file. You
can add new entries if you need to cite references that are not included yet.


Including images and figures
""""""""""""""""""""""""""""

It is possible to include static images from the ``sorbetto/doc/images``
directory in the documentation. The syntax is as follows:

.. code-block:: rst

    .. image:: /images/<your image name>

You can also use software-generated figures (see below) from the
``sorbetto/doc/figures`` directory:

.. code-block:: rst

    .. image:: /figures/<your figure name>

Most commonly used image formats are allowed, but we recommend svg files when
possible for size and resolution.


Generating figures
^^^^^^^^^^^^^^^^^^

In order to include software-generated figures in the documentation, you must
create a script in ``sorbetto/doc/scripts``. All the Python scripts in that
directory are automatically detected and run in order to generate the figures
for the documentation. They must be saved in the correct directory to be
accessible from the documentation: ``sorbetto/doc/figures``.

In order to facilitate this process, we provide the
``sorbetto/doc/scripts/utils.py`` helper script which implements a
``run_and_save`` function. If called with a plotting function, it will run it
and save the resulting figure in the correct directory.  If the figure already
exists, it will be skipped to speed up execution. Therefore, you should delete
any existing figures that you wish to replace or generate anew before running
the scripts.

You can automatically generate all figures as follows:

.. code-block:: bash

    cd doc
    make figures

You can check that all figures were correctly generated under
``sorbetto/doc/figures/``.


Adding new demos and examples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :ref:`Demos` and :ref:`Examples` sections are automatically populated by
scanning the ``sorbetto/demos`` and ``sorbetto/examples`` respectively for
Python notebooks. You can simply add yours in the relevant directory to include
it in the documentation. **A notebook must have a main heading in a markdown
cell to be referenced in the table of contents.** Notebooks will be uploaded to
the documentation "as is", so make sure to run them and save them in a clean
state for best results (if a notebook is uploaded without having been run, the
documentation build step will attempt to run it entirely, which could cause
errors).

Examples are listed in a gallery. The last image output of the notebook will
be automatically selected as thumbnail. If you wish to select a different
thumbnail, visit the `nbsphinx documentation
<https://nbsphinx.readthedocs.io/en/latest/subdir/gallery.html>`__ for more
instructions.


Building the documentation locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to build the documentation, you need to install additional dependencies
first (you can skip the cloning step if you already did it):

.. code-block:: bash

    git clone https://github.com/uliege-performance/sorbetto.git
    cd sorbetto
    pip install -e ".[docs]"

Apart from the automatically installed dependencies, you also need to install
Pancod. Follow the instructions on the `Pandoc documentation
<https://pandoc.org/installing.html>`__

Once your environment is set up and you have all the figures (see `Generating
figures`_), you can build the documentation locally as follows:

.. code-block:: bash

    cd doc
    make html

The resulting documentation in html format will be located at
``sorbetto/doc/_build/html/index.html``.


Running tests
-------------

The directory ``sorbetto/tests`` contains unit tests to automatically check the
validity of the core implementation of the library. To launch the tests locally,
run this command in the root directory of Sorbetto:

.. code-block:: bash

    pytest

Please check that all tests are passing before submitting a new contribution.
Also, it is best to create new tests if you implement a new functionality.
Check the `pytest documentation <https://docs.pytest.org/en/stable/>`__ if you
need more information on how to write tests.


Manually building and publishing the library
--------------------------------------------

You can build and publish the library manually if needed, to check that
everything is ready before a release for example. To do so, you need to install
specific dependencies (omit the cloning if already done):

.. code-block:: bash

    git clone https://github.com/uliege-performance/sorbetto.git
    cd sorbetto
    pip install -e ".[dist]"

Then create the wheels:

.. code-block:: bash

    python -m build

The build outputs will be located under ``sorbetto/dist``. You can then upload
them to the PyPI test repository as follows:

.. code-block:: bash

    twine upload --repository testpypi dist/sorbetto-*

After checking that everything works as expected, you can upload it to PyPI by
removing the ``--repository testpypi`` option. Ideally, this step should be
automated and not done manually.
