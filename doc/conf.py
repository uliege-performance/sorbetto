# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "sorbetto"
copyright = "2025, Sebastien Pierard et al."
author = "Sebastien Pierard et al."

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.mathjax",
    "sphinx_math_dollar",
    "sphinxcontrib.bibtex",
    "nbsphinx",
    "sphinx_gallery.load_style",
    # TODO uncomment when nbsphinx will support Sphinx 8.2
    # "sphinx.ext.apidoc",
    # TODO remove when nbsphinx will support Sphinx 8.2
    "sphinxcontrib.apidoc",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# TODO uncomment when nbsphinx will support Sphinx 8.2
# apidoc_modules = [
#     {
#         "path": "../../sorbetto",
#         "destination": "api",
#         "separate_modules": True,
#         "no_headings": False,
#         "module_first": True,
#         "max_depth": 1,
#         "automodule_options": {
#             "members",
#             "undoc-members",
#             "show-inheritance",
#         },
#     }
# ]

# TODO remove when nbsphinx will support Sphinx 8.2
apidoc_module_dir = "../../sorbetto"
apidoc_output_dir = "api"
apidoc_separate_modules = True
apidoc_module_first = True
apidoc_toc_file = False
apidoc_extra_args = ["-d", "1"]
autodoc_default_options = {
    "show-inheritance": True,
    "undoc-members": True,
    "members": True,
}


mathjax3_config = {
    "tex": {
        "inlineMath": [["\\(", "\\)"]],
        "displayMath": [["\\[", "\\]"]],
    }
}

bibtex_bibfiles = ["references.bib"]
bibtex_default_style = "plain"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
# html_static_path = ["_static"]
html_logo = "src/images/sorbetto_banner.svg"
html_theme_options = {
    "logo_only": True,
}
