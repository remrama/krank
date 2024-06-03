=====
Krank
=====


Fetch psychology datasets from remote sources.

.. important::

   Refer to `Krank's online documentation <https://remrama.github.io/krank>`_ for the most comprehensive and up-to-date description of features and functions.


**Krank** is a single-stop for using publicly available remote datasets. It offers simplified downloading, storing, version controlling, loading into Python, minimal/corrective pre-processing, and in some cases, data harmonization of various datasets. This project has a huge dependency on the `Pooch <https://www.fatiando.org/pooch>`_ Python package, which makes retrieving and storing any remote file incredibly easy.


.. warning::

   This project is in the planning stage of development. Don't use it.


**Krank** currently has a limited set of modules that are each dedicated to a specific type of dataset. The topical focus of these datasets is probably *psychology* or *cognitive neuroscience*. The datasets are grouped into separate modules for organizational purposes, where each module focuses on a specific type of dataset. Each module functions almost identically, and the separation of fetching functions into these separate modules is primarily for organizational purposes.

Currently implemented modules include:

* ``tables``: Fetch tables that were manually extracted from journal publications.
* ``lexicons``: Fetch lexicons that contain vocabularies with associated numerical scores.
* ``liwc``: Fetch previously published or shared LIWC scores/output.



Installation
------------

.. code-block:: shell

   pip install --upgrade krank



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



Contributing
------------

Currently, Krank is developed mostly for my own personal desires for more convenient data access, more convenient data storage, a better ability to see a high-level view of all the datasets available for my projects, and better version-control over the public datasets I use and create. Making a Python package with documentation to view the datasets seemed like the best way to do this.

That being said, if anyone else finds it useful and wants to contribute, please do. Feel free to post questions, bugs, feature requests, new dataset proposals, or even new module proposals on the `Krank GitHub Issues page <https://github.com/remrama/krank/issues>`_.
