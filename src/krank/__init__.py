from .readers import *

__version__ = "0.0.0+dev"


def read(krank_id):
    from . import readers
    krank_reader = getattr(readers, f"read_{krank_id}")
    dreams, dreamers = krank_reader()
    return dreams, dreamers
