# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from pathlib import Path
import time
import sys

from importlib.metadata import metadata

# Need to make sure that krank can be imported, and also that
# it is importing the local one (as opposed to a previously pip installed one).
# So this can be from the krank/src/krank directory or through a locally
# built or locally pip installed version.
#
# This prevents the need to build krank manually in the github action for pages.
#
# autodoc needs to import your modules in order to extract the docstrings.
# Therefore, you must add the appropriate path to sys.path in your conf.py.
sys.path.insert(0, str(Path(__file__).parents[1].joinpath("src")))
import krank


project = krank.__name__
release = krank.__version__  # Full project version
version = krank.__version__[:3]  # Major project version
author = metadata("krank").get("Author-email").split(" <")[0]
curryear = time.strftime("%Y")
copyright = f"2024-{curryear}, {author}"


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # "sphinx.ext.doctest",
    # "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",  # Core Sphinx library for auto html doc generation from docstrings
    "sphinx.ext.autosummary",  # Create neat summary tables for modules/classes/methods etc
    "sphinx.ext.intersphinx",  # Link to other project's documentation (see mapping below)
    # "sphinx_autodoc_typehints",  # Automatically document param types (less noise in class signature)
    # "numpydoc",
    # "sphinx_copybutton",  # Adds a copy button to code blocks (for pasting)
    "sphinx.ext.autosectionlabel",
    # "sphinx.ext.linkcode",
]

# sphinx.ext.autosectionlabel option
# Make sure the target is unique
autosectionlabel_prefix_document = True
# autosectionlabel_maxdepth = 1

source_suffix = ".rst"
source_encoding = "utf-8"
# master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
# include_patterns = "**"
templates_path = ["_templates"]
# rst_epilog = """"""
# rst_prolog = """"""
# keep_warnings = False
# show_warning_types = False
# numfig = False
# pygments_style = "default"
# add_function_parentheses = True
# add_module_names = False
# toc_object_entries = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_title = f"Krank v{release}"  # defaults to "<project> v<revision> documentation"
html_short_title = "Krank"
html_logo = None
html_favicon = None
html_css_files = []
html_static_path = ["_static"]
html_last_updated_fmt = ""  # empty string is equivalent to "%b %d, %Y"
html_permalinks = True
html_domain_indices = True
html_use_index = False
html_show_sourcelink = False
html_show_copyright = False
html_show_sphinx = False
html_output_encoding = "utf-8"
html_sidebars = {
    #     "**": ["localtoc.html", "globaltoc.html", "searchbox.html"],
    "**": [],  # to remove primary sidebar from all pages
}
# html_additional_pages = {}
# :html_theme.sidebar_secondary.remove: true

# I think this is just for showing source?
html_context = {
    # "github_url": "https://github.com",
    "github_user": "remrama",
    "github_repo": "krank",
    "github_version": "main",
    "doc_path": "docs",
    "default_mode": "auto",  # light, dark, auto
}

html_theme_options = {
    "navigation_with_keys": False,
    "external_links": [
        {"name": "Releases", "url": "https://github.com/remrama/krank/releases"},
        {
            "name": "Contributing",
            "url": "https://github.com/remrama/krank#contributing",
        },
    ],
    "header_links_before_dropdown": 4,
    "navbar_start": ["navbar-logo", "navbar-icon-links"],  # "version-switcher"
    "navbar_center": ["navbar-nav"],
    "navbar_end": [],
    # "navbar_persistent": [],  # Default is a nice search bubble that I otherwise don't get
    "search_bar_text": "Search...",
    # "article_header_start": ["breadcrumbs"],
    # "article_header_end": [],
    # "article_footer_items": [],
    "footer_start": ["last-updated"],  # "search-field" "search-button"
    "footer_center": [],
    "footer_end": [],  # "theme-switcher"
    "content_footer_items": [],
    "show_prev_next": False,
    # "sidebarwidth": 230,
    # "navbar_start": ["navbar-logo", "version-switcher"],
    "show_version_warning_banner": True,
    "announcement": "BEWARE! <a href='https://github.com/remrama/krank'>This project</a> is in the planning stage. DO NOT USE!",
    "navbar_align": "left",  # [left, content, right] For testing that the navbar items align properly
    "show_nav_level": 3,
    "show_toc_level": 3,
    "navigation_depth": 3,
    "collapse_navigation": False,
    # "secondary_sidebar_items": [],
    # "secondary_sidebar_items": {"**": []},
    "use_edit_page_button": False,
    # "use_repository_button": True,
    # "icon_links_label": "Quick Links",
    "icon_links": [
        {
            "name": "Krank on GitHub",
            "url": "https://github.com/remrama/krank",
            "icon": "fa-brands fa-square-github",
            "type": "fontawesome",
        },
    ],
}

# configure sphinx-copybutton
# https://github.com/executablebooks/sphinx-copybutton
# copybutton_prompt_text = r">>> |\.\.\. |\$ "
# copybutton_prompt_is_regexp = True


# -- Options for autosummary/autodoc output ------------------------------------
# Generate the API documentation when building
autosummary_generate = True  # Turn on sphinx.ext.autosummary
# autodoc_typehints = "description"
# autodoc_member_order = "groupwise"
autodoc_default_options = {
    "members": True,
    "member-order": "groupwise",
    "undoc-members": False,
    # "special-members": "__init__",
    # "exclude-members": "__weakref__",
}


# -- Intersphinx ------------------------------------------------

intersphinx_mapping = {
    "krank": ("https://remrama.github.io/krank", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    "pooch": ("https://www.fatiando.org/pooch/latest", None),
    "python": ("https://docs.python.org/3", None),
}
