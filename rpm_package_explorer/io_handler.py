# read 128 kB
import io
from typing import Union


def read_data(file_object: Union[io.FileIO, io.BytesIO], read_size=128*1024):
    while True:
        data = file_object.read(read_size)
        if not data:
            break
        yield data


