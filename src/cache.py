import shelve
import tempfile
import os


def get_cache_path(label):
    return os.path.join(tempfile.gettempdir(), '{}.pickle'.format(label))


def open(label, **kwargs):
    cachePath = get_cache_path(label)
    shelf = shelve.open(cachePath, **kwargs)
    return shelf
