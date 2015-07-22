import pickle


def read(path):
    try:
        cacheFile = open(path, 'rb')
    except IOError:
        return None
    else:
        try:
            obj = pickle.load(cacheFile)
        except EOFError:
            return None
        else:
            return obj
        finally:
            cacheFile.close()


def write(path, obj):
    with open(path, 'wb+') as cacheFile:
        pickle.dump(obj, cacheFile, pickle.HIGHEST_PROTOCOL)
