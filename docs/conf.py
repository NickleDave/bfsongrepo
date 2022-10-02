# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'bfsongrepo'
copyright = '2022, David Nicholson'
author = 'David Nicholson'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_nb",
    'sphinx_copybutton',
    "sphinx_design",
    'sphinxext.opengraph',
    'sphinx_tabs.tabs',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = []

source_suffix = '.md'

master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_static_path = ['_static']

# -- theme configuration -----------------------------------------------

html_theme = 'pydata_sphinx_theme'

html_theme_options = {
  "show_toc_level": 3
}

html_title = "Bengalese Finch Song Repository"

# -- myst configuration -------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "linkify",
    "replacements",
]

myst_heading_anchors = 3

nb_execution_excludepatterns = 'scripts/*'