# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sphinx_rtd_theme


project = "Pauli Strings Python"
copyright = "2025, Nicolas Loizeau"
author = "Nicolas Loizeau"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx_github_style",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"


html_context = {
    "display_github": True,
    "github_user": "nicolasloizeau",
    "github_repo": "PauliStrings.py",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

pygments_style = "friendly"

html_logo = "_static/logo_cat_small.svg"
html_favicon = "_static/favicon.png"
html_css_files = [
    "custom.css",
]
