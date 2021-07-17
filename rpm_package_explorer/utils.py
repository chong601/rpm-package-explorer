import bz2
import gzip
import lzma
import sqlite3


def open_file(filename: str, mode='r', encoding=None):
    """Get the file extension and process the file based on the file extension
    Else, open the file using the provided encoding spec or just do
    ASCII-based read

    WARNING: This code DO NOT check if the provided mode and encoding will
    not raise an exception from underlying open() call.

    :param filename: The name of the file to be opened
    :param mode: The mode of how the file should be handled
    :param encoding: The encoding that the data should be handled

    :returns: File object for the filename in their respective file object type
    """
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
    """
    Just a neat function that converts cursor tuple-y data into dictionary

    :param cursor: The cursor after a query is executed
    :param row_data: The row data after the query is executed
    :returns: A dictionary of the query data in the form of {column_name: row_data}
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row_data[idx]
    return d
