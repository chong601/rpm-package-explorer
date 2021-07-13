import bz2
import gzip
import lzma


def open_file(filename: str, mode='r'):
    file_ext = filename.rsplit('.', 1)[-1]
    if file_ext == 'gz':
        return gzip.open(filename)
    elif file_ext == 'bz2':
        return bz2.open(filename)
    elif file_ext == 'xz':
        return lzma.open(filename)
    else:
        return open(filename, mode)

