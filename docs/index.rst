
.. image:: https://badge.fury.io/py/krank.svg
   :target: https://badge.fury.io/py/krank
   :alt: PyPI


----


Krank
=====


Fetch psychology datasets from remote sources.

**Krank** is a single-stop for using publicly available remote datasets. It offers simplified downloading, storing, version controlling, loading into Python, minimal/corrective pre-processing, and in some cases, data harmonization of various datasets. This project has a huge dependency on the `Pooch <https://www.fatiando.org/pooch>`_ Python package, which makes retrieving and storing any remote file incredibly easy.

See Krank's :doc:`api` for a complete list of currently available functions.

Feel free to post questions, bugs, feature requests, new dataset proposals, or even new module proposals on the `Krank GitHub Issues page <https://github.com/remrama/krank/issues>`_. See :doc:`contributing` for more details.


.. danger::

   This project is in the planning stage of development. DO NOT USE!


.. toctree::
   :maxdepth: 1
   :caption: Contents

   api.rst


Installation
------------

.. code-block:: shell

   pip install krank



Modules
-------

**Krank** currently has a limited set of modules that are each dedicated to a specific type of dataset. The topical focus of these datasets is probably *psychology* or *cognitive neuroscience*. The datasets are grouped into separate modules for organizational purposes, where each module focuses on a specific type of dataset. Each module functions almost identically, and the separation of fetching functions into these separate modules is primarily for organizational purposes. Currently implemented modules include:

* :ref:`api:tables`: Fetch tables that were manually extracted from journal publications.
* :ref:`api:lexicons`: Fetch lexicons that contain vocabularies with associated numerical scores.
* :ref:`api:liwc`: Fetch previously published or shared LIWC scores/output.



Usage
-----

Fetch (i.e., download) the `threat` LIWC dictionary, described in `Choi et al., 2022, PNAS <https://doi.org/10.1073/pnas.2113891119>`_  and shared publicly via `Michele Gelfand's personal website <https://www.michelegelfand.com/threat-dictionary>`_.

.. code-block:: python

   from krank import lexicons

   df = lexicons.fetch_threat()


An identical way to fetch the same file is through krank's top-level interface, which offers a more general way to retrieve datasets and might be more convenient for looping over a large number of datasets to load them systematically.

.. code-block:: python

   import krank

   df = krank.fetch_lexicon("threat")
