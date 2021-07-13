import declxml as xml
import json
from typing import Union
from io import BytesIO, FileIO


def parse_repomd(filename: str):
    data_processor = xml.array(xml.dictionary('data', [
        xml.string('.', attribute='type'),
        xml.string('checksum', 'type', alias='checksum_hash_type'),
        xml.string('checksum', alias='checksum_hash'),
        xml.string('open-checksum', 'type', alias='open_checksum_hash_type', default=None, required=False),
        xml.string('open-checksum', alias='open_checksum_hash', default=None, required=False),
        xml.string('location', attribute='href'),
        xml.integer('timestamp'),
        xml.integer('size'),
        xml.integer('open-size', default=None, alias='open_size', required=False),
        xml.integer('database_version', default=None, required=False)
    ]))
    repomd_processor = xml.dictionary('repomd', [data_processor])
    return rearrange_data(xml.parse_from_file(repomd_processor, filename))


def rearrange_data(xml_dict: dict):
    # Recast to dict rather than ItemsView
    new_dict = {}
    # .values always return an array even for single item, so we get the first element
    dict_value = list(xml_dict.values())[0]
    for d in dict_value:
        d: dict
        repo_type = d['type']
        del d['type']
        new_dict.update({repo_type: d})

    return new_dict
