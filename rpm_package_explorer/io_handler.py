# read 128 kB
import io
from typing import Union


# Use more memory-efficient buffered read method
def read_data(file_object: Union[io.FileIO, io.BytesIO], read_size=128*1024):
    """
    Generator function to read data from the file object and returns data based on the provided read size.

    :param file_object: File object to read data from
    :param read_size: The size of the data to be read at a time in bytes
    :returns: The data from the file object in `read_size` chunks until it reaches the end of file
    """
    while True:
        data = file_object.read(read_size)
        if not data:
            break
        yield data
