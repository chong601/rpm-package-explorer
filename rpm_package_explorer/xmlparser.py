import declxml as xml
import json


def parse_repomd(filename: str):
    with open(filename) as example_xml:
        data_processor = xml.array(xml.dictionary('data', [
            xml.string('.', attribute='type'),
            xml.string('checksum', 'type', alias='checksum_hash_type'),
            xml.string('checksum', alias='checksum_hash'),
            xml.string('open-checksum', 'type', alias='open_checksum_hash_type', required=False),
            xml.string('open-checksum', alias='open_checksum_hash', required=False),
            xml.string('location', attribute='href'),
            xml.integer('timestamp'),
            xml.integer('size'),
            xml.integer('open-size', required=False),
            xml.integer('database_version', required=False, default=None)
        ]))
        repomd_processor = xml.dictionary('repomd', [data_processor])
        print(json.dumps(xml.parse_from_string(repomd_processor, example_xml.read()), indent=2))
