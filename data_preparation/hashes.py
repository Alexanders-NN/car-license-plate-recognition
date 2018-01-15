import hashlib


def get_hashers(*args):
    hdict = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha224': hashlib.sha224,
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha384,
        'sha512': hashlib.sha512
    }

    result = {}
    for arg in args:
        if arg in hdict:
            result[arg] = hdict[arg]()
        else:
            raise Exception("Unknown hash method : {}".format(arg))
    return result

def update_hashers(hashers, data):
    for m in hashers:
        hashers[m].update(data)
    return hashers

def hashers_result(hashers):
    return {h: hashers[h].hexdigest() for h in sorted(hashers.keys())}


def file_hash(filename, *args):
    hashers = hashers_result(
            update_hashers(
                get_hashers(*args),
                open(filename, 'rb').read()
                )
        )
    result = []
    for m in args:
        result.append(hashers[m])
    return tuple(result)
