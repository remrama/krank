.. |heading| replace:: ``repositories``

.. currentmodule:: krank

|heading|
---------

The ``repositories`` module provides access to various dream-related data repositories. Initiate a repository, or :class:`~krank.repositories._base.KrankRepo`, to fetch raw files and load them in tidy format.

Each repository is different, but all have a few overlapping features.
Each repository has a :meth:`~krank.repositories._base.KrankRepo.read_file` method that can be used to read individual raw files.

The primary benefit is the :meth:`~krank.repositories._base.KrankRepo.read_tidy` method attached to each repository, which can be used to load cleaned up dream datasets in tidy format.


.. autosummary::
   :toctree: generated/
   :nosignatures:

   repositories.Samson2023
   repositories.DreamBank
