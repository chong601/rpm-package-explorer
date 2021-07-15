import bz2
import gzip
import lzma
import sqlite3


def open_file(filename: str, mode='r', encoding=None):
    file_ext = filename.rsplit('.', 1)[-1]
    if file_ext == 'gz':
        return gzip.open(filename)
    elif file_ext == 'bz2':
        return bz2.open(filename)
    elif file_ext == 'xz':
        return lzma.open(filename)
    elif encoding is not None:
        return open(filename, mode, encoding=encoding)
    else:
        return open(filename, mode)


def map_row_to_dict(cursor: sqlite3.Cursor, row_data):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row_data[idx]
    return d
