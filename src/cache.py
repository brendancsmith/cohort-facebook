import shelve
import tempfile
import os


def generate_cache_path(label):
    return os.path.join(tempfile.gettempdir(), '{}.pickle'.format(label))


def find(label, **kwargs):
    cachePath = generate_cache_path(label)
    shelf = shelve.open(cachePath, **kwargs)
    return shelf
