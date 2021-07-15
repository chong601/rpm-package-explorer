import declxml as dxml
from rpm_package_explorer.utils import open_file


def parse_repomd(filename: str):
    data_processor = dxml.array(dxml.dictionary('data', [
        dxml.string('.', attribute='type'),
        dxml.string('checksum', 'type', alias='checksum_hash_type'),
        dxml.string('checksum', alias='checksum_hash'),
        dxml.string('open-checksum', 'type', alias='open_checksum_hash_type', default=None, required=False),
        dxml.string('open-checksum', alias='open_checksum_hash', default=None, required=False),
        dxml.string('location', attribute='href'),
        dxml.integer('timestamp'),
        dxml.integer('size'),
        dxml.integer('open-size', default=None, alias='open_size', required=False),
        dxml.integer('database_version', default=None, required=False)
    ]))
    repomd_processor = dxml.dictionary('repomd', [data_processor])
    return rearrange_data(dxml.parse_from_file(repomd_processor, filename), 'type')


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


def parse_filelists(filename: str):
    package_processor = dxml.array(dxml.dictionary(
        'package', [
            dxml.string('.', 'pkgid'),
            dxml.string('.', 'name'),
            dxml.string('.', 'arch'),
            dxml.integer('version', 'epoch'),
            dxml.string('version', 'ver', alias='version'),
            dxml.string('version', 'rel', alias='release'),
            dxml.array(
                dxml.dictionary('file', [
                    dxml.string('.', 'type', default='file', required=False),
                    dxml.string('.', alias='name')
                ], required=False))
        ]))
    filelists_processor = dxml.dictionary('filelists', [package_processor])
    return dxml.parse_from_file(filelists_processor, filename)


def parse_otherdata(filename: str):
    package_processor = dxml.array(dxml.dictionary(
        'package', [
            dxml.string('.', 'pkgid'),
            dxml.string('.', 'name'),
            dxml.string('.', 'arch'),
            dxml.integer('version', 'epoch'),
            dxml.string('version', 'ver', alias='version'),
            dxml.string('version', 'rel', alias='release'),
            dxml.array(
                dxml.dictionary('changelog', [
                    dxml.string('.', 'author'),
                    dxml.integer('.', 'date'),
                    dxml.string('.', alias='changelog')
                ], required=False))
        ]))
    otherlist_processor = dxml.dictionary('otherdata', [package_processor])
    return dxml.parse_from_file(otherlist_processor, filename)


def parse_updateinfo(filename: str):
    reference_processor = dxml.dictionary('reference', [
        dxml.string('.', 'href'),
        dxml.string('.', 'id'),
        dxml.string('.', 'type'),
        dxml.string('.', 'title')
    ], required=False)

    package_processor = dxml.dictionary('package', [
        dxml.string('.', 'name', alias='name'),
        dxml.string('.', 'version', alias='version'),
        dxml.string('.', 'release', alias='release'),
        dxml.integer('.', 'epoch', alias='epoch'),
        dxml.string('.', 'arch', alias='arch'),
        dxml.string('.', 'src', alias='src'),
        dxml.string('filename'),
        dxml.string('sum', 'type', alias='hash_type'),
        dxml.string('sum', alias='hash')
    ])

    collection_processor = dxml.dictionary('pkglist/collection', [
        dxml.string('.', 'short', alias='collection_shortname'),
        dxml.string('name'),
        dxml.array(package_processor)
    ])

    update_processor = dxml.array(dxml.dictionary(
        'update', [
            dxml.string('.', 'from'),
            dxml.string('.', 'status'),
            dxml.string('.', 'type'),
            dxml.integer('.', 'version'),
            dxml.string('id'),
            dxml.string('title'),
            dxml.string('issued', 'date', alias='issued_date'),
            dxml.string('updated', 'date', alias='updated_date'),
            dxml.string('rights'),
            dxml.integer('release'),
            dxml.integer('pushcount'),
            dxml.string('severity'),
            dxml.string('summary'),
            dxml.string('description'),
            dxml.array(reference_processor, nested='references'),
            dxml.array(collection_processor, alias='collection')
        ]))
    updates_processor = dxml.dictionary('updates', [update_processor])
    return dxml.parse_from_file(updates_processor, filename)


def parse_primary(filename: str):
    version_processor = dxml.dictionary('version', [
        dxml.integer('.', 'epoch', alias='epoch'),
        dxml.string('.', 'ver', alias='ver'),
        dxml.string('.', 'rel', alias='rel')
    ])

    checksum_processor = dxml.dictionary('checksum', [
        dxml.string('.', 'type', alias='type'),
        dxml.string('.', alias='pkgid')
    ])

    time_processor = dxml.dictionary('time', [
        dxml.integer('.', 'file', 'file'),
        dxml.integer('.', 'build')
    ])

    size_processor = dxml.dictionary('size', [
        dxml.integer('.', 'package'),
        dxml.integer('.', 'installed'),
        dxml.integer('.', 'archive')
    ])

    location_processor = dxml.dictionary('location', [
        dxml.string('.', 'href')
    ])

    header_range_processor = dxml.dictionary('header-range', [
        dxml.integer('.', 'start'),
        dxml.integer('.', 'end')
    ])

    provides_processor = dxml.array(dxml.dictionary('entry', [
        dxml.string('.', 'name'),
        dxml.string('.', 'flags', required=False, default=None),
        dxml.integer('.', 'epoch', required=False, default=None),
        dxml.string('.', 'ver', required=False, default=None),
        dxml.string('.', 'rel', required=False, default=None)
    ], required=False), nested='provides')

    requires_processor = dxml.array(dxml.dictionary('entry', [
        dxml.string('.', 'name'),
        dxml.string('.', 'flags', required=False, default=None),
        dxml.integer('.', 'epoch', required=False, default=None),
        dxml.string('.', 'ver', required=False, default=None),
        dxml.string('.', 'rel', required=False, default=None),
        dxml.integer('.', 'pre', required=False, default=None)
    ], required=False), nested='requires')

    conflicts_processor = dxml.array(dxml.dictionary('entry', [
        dxml.string('.', 'name'),
        dxml.string('.', 'flags', required=False, default=None),
        dxml.integer('.', 'epoch', required=False, default=None),
        dxml.string('.', 'ver', required=False, default=None),
        dxml.string('.', 'rel', required=False, default=None)
    ], required=False), nested='conflicts')

    format_processor = dxml.dictionary('format', [
        dxml.string('license'),
        dxml.string('vendor'),
        dxml.string('group'),
        dxml.string('buildhost'),
        dxml.string('sourcerpm'),
        header_range_processor,
        provides_processor,
        requires_processor,
        conflicts_processor
    ])

    package_processor = dxml.array(dxml.dictionary('package', [
        dxml.string('name'),
        dxml.string('arch'),
        version_processor,
        checksum_processor,
        dxml.string('summary'),
        dxml.string('description'),
        dxml.string('packager'),
        dxml.string('url'),
        time_processor,
        size_processor,
        location_processor,
        format_processor
    ]))

    metadata_processor = dxml.dictionary('metadata', [package_processor])
    return dxml.parse_from_file(metadata_processor, filename)


def parse_groups(filename: str):
    # Oh cock this one has fucking DTD
    # So I have few ways to do it:
    # - ignore comps file forever (which I prefer **not** to)
    # - compile libcomps and use that instead (too much effort)
    # - do it the hard way and learn lxml (ugh)
    # - or jank it
    #
    # HMMMMMMMMMMMMMMMMMMM.
    
    # BEGIN jank
    new_filename = filename.replace('comps', 'compsnew')
    with open_file(filename, encoding='utf8') as src_file, open_file(new_filename, 'w', encoding='utf8') as dest_file:
        for line in src_file.readlines():
            if line.find('DOCTYPE comps') != -1 or line.find('DTD Comps info') != -1 or line.find('comps.dtd') != -1:
                continue
            dest_file.writelines(line.replace('xml:', ''))
    # END jank

    group_processor = dxml.array(dxml.dictionary('group', [
        dxml.string('id'),
        dxml.array(dxml.dictionary('name', [
            dxml.string('.', 'lang', default='en', required=False),
            dxml.string('.', alias='content')
        ], alias='entry'), alias='name'),
        dxml.array(dxml.dictionary('description', [
            dxml.string('.', 'lang', default='en', required=False),
            dxml.string('.', alias='content')
        ], alias='entry'), alias='description'),
        dxml.boolean('default'),
        dxml.boolean('uservisible'),
        dxml.dictionary('packagelist', [
            dxml.array(dxml.dictionary('packagereq', [
                dxml.string('.', 'type'),
                dxml.string('.', alias='package_name')
            ]))
        ])
    ]))
    comps_processor = dxml.dictionary('comps', [group_processor])

    return dxml.parse_from_file(comps_processor, new_filename)
