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
    return rearrange_data(xml.parse_from_file(repomd_processor, filename), 'type')


def rearrange_data(xml_dict: dict, key_name):
    # Recast to dict rather than ItemsView
    new_dict = {}
    # .values always return an array even for single item, so we get the first element
    dict_value = list(xml_dict.values())[0]
    for d in dict_value:
        d: dict
        key = d[key_name]
        del d[key_name]
        new_dict.update({key: d})

    return new_dict

def parse_filelists():
    package_processor = xml.array(xml.dictionary(
        'package', [
            xml.string('.', 'pkgid'),
            xml.string('.', 'name'),
            xml.string('.', 'arch'),
            xml.integer('version', 'epoch'),
            xml.string('version', 'ver', alias='version'),
            xml.string('version', 'rel', alias='release'),
            xml.array(
                xml.dictionary('file', [
                    xml.string('.', 'type', default='file', required=False, omit_empty=True),
                    xml.string('.', alias='name')
                ]))
        ]))
    filelists_processor = xml.dictionary('filelists', [package_processor])
    return rearrange_data(xml.parse_from_string(filelists_processor, xml_data), key_name='pkgid')
