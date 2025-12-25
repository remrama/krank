
.. danger::

   This project is in the planning stage of development. DO NOT USE!


.. image:: https://www.repostatus.org/badges/latest/concept.svg
   :target: https://www.repostatus.org/#concept
   :alt: Project Status: Concept – Minimal or no implementation has been done yet

.. image:: https://img.shields.io/github/license/dxelab/dreambank.svg
   :target: https://github.com/dxelab/dreambank/blob/master/LICENSE
   :alt: License

.. image:: https://badge.fury.io/py/dreambank.svg
   :target: https://badge.fury.io/py/dreambank
   :alt: PyPI

.. image:: https://pepy.tech/badge/dreambank/month
   :target: https://pepy.tech/badge/dreambank/month
   :alt: Downloads

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black

.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://github.com/astral-sh/ruff
   :alt: Ruff

.. image:: https://github.com/dxelab/dreambank/actions/workflows/docs.yml/badge.svg
  :target: https://github.com/dxelab/dreambank/actions
  :alt: Docs test

.. image:: https://github.com/remrama/krank/actions/workflows/black.yml/badge.svg
   :target: https://github.com/remrama/krank/actions
   :alt: Lint & Format (Style)


---


krank
=====


Fetch psychology datasets from remote sources.

|krank| is a single-stop for using publicly available remote datasets. It offers simplified downloading, storing, version controlling, loading into Python, minimal/corrective pre-processing, and in some cases, data harmonization of various datasets. This project has a huge dependency on the `Pooch <https://www.fatiando.org/pooch>`_ Python package, which makes retrieving and storing any remote file incredibly easy.

|krank| currently has a limited set of modules that are each dedicated to a specific type of dataset. The topical focus of these datasets is probably *psychology* or *cognitive neuroscience*. The datasets are grouped into separate modules for organizational purposes, where each module focuses on a specific type of dataset. Each module functions almost identically, and the separation of fetching functions into these separate modules is primarily for organizational purposes. Currently implemented modules include:

* :doc:`krank`: Top-level access to generalized functions to access each module.
* :doc:`repositories`: Fetch tables that were manually extracted from journal publications.

See the |krank| :doc:`api` reference page for a complete list of currently available functions.


Feel free to post questions, bugs, feature requests, new dataset proposals, or even new module proposals on the |krank| `GitHub Issues page <https://github.com/remrama/krank/issues>`_. See :doc:`contributing` for more details.


.. Links to internal docs that will show up in the navigation bar.
.. :hidden: Hides it from displaying on the current index.rst page but adds to Sections.
.. toctree::
   :maxdepth: 2
   :hidden:

   api
   usage
   contributing
