# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import django
from django.conf import settings

sys.path.insert(0, os.path.abspath(".."))  # so that we can access the "django_migration_zero" package
settings.configure(
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django_migration_zero",
    ],
    SECRET_KEY="ASDFjklö123456890",
)
django.setup()

from django_migration_zero import __version__  # noqa: E402

# -- Project information -----------------------------------------------------

project = "django-migration-zero"
copyright = "2024, Ambient Innovation: GmbH"  # noqa: A001
author = "Ambient Digital <hello@ambient.digital>"
version = __version__
release = __version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "m2r2",
]

source_suffix = [".rst", ".md"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "display_version": False,
    "style_external_links": False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Set master doc file
master_doc = "index"
