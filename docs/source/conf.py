# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "BEC"
copyright = "2022, Paul Scherrer Institute, Switzerland"
author = "Klaus Wakonig"
release = "0.1"

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scan_bundler")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../scan_server")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../bec_client")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../bec_utils")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../file_writer")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../device_server")))

extensions = [
    "sphinx.ext.autodoc",  # Core library for html generation from docstrings
    "sphinx.ext.autosummary",  # Create neat summary tables
    "sphinx.ext.todo",
    "recommonmark",
    "sphinx_copybutton",
]
autosummary_generate = True  # Turn on sphinx.ext.autosummary
add_module_names = False  # Remove namespaces from class/method signatures
autodoc_inherit_docstrings = True  # If no docstring, inherit from base class
set_type_checking_flag = True  # Enable 'expensive' imports for sphinx_autodoc_typehints
autoclass_content = "both"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "Python"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
# html_theme_options = {
#     "switcher": {
#         "json_url": "https://beamline-experiment-control.readthedocs.io/en/latest/_static/switcher.json",
#         "version_match": "master",
#     },
#     "navbar_start": ["navbar-logo", "version-switcher"],
# }
