import declxml as dxml
from .utils import open_file


def parse_repomd(filename: str):
    """
    Read and return the repomd data

    Data returned will be in the form of Python dictionary such as:s
    {
        type: {
            checksum_hash_type: hash_type,
            checksum_hash: hash,
            ...
        }
    }

    :param filename: The repomd file name
    :returns: parsed XML data in the form of a Python dictionary
    """
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
    """
    Converts a list of Python dictionary into just dictionary with key_name as the key name
    """
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
    """Parse filelists XML data into Python dictionary form"""
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
    """Parse other xml data into Python dictionary form"""
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
    """Parse updateinfo data into Python dictionary form"""
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
    """Parse primary XML data and returns it in Python dictionary form"""
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

    package_meta = [
        dxml.string('.', 'name'),
        dxml.string('.', 'flags', required=False, default=None),
        dxml.integer('.', 'epoch', required=False, default=None),
        dxml.string('.', 'ver', required=False, default=None),
        dxml.string('.', 'rel', required=False, default=None)
    ]

    provides_processor = dxml.array(dxml.dictionary('entry', package_meta, required=False), nested='provides')

    requires_meta = package_meta.copy()
    requires_meta.append(dxml.integer('.', 'pre', required=False, default=None))
    requires_processor = dxml.array(dxml.dictionary('entry', requires_meta, required=False), nested='requires')

    conflicts_processor = dxml.array(dxml.dictionary('entry', package_meta, required=False), nested='conflicts')

    enhances_processor = dxml.array(dxml.dictionary('entry', package_meta, required=False), nested='enhances')

    files_processor = dxml.array(dxml.dictionary('file', [
        dxml.string('.'),
        dxml.string('.', 'type', required=False, default='file')
    ], required=False))

    obsoletes_processor = dxml.array(dxml.dictionary('entry', package_meta, required=False), nested='obsoletes')

    recommends_processor = dxml.array(dxml.dictionary('entry', package_meta, required=False), nested='recommends')

    suggests_processor = dxml.array(dxml.dictionary('entry', package_meta, required=False), nested='suggests')

    supplements_processor = dxml.array(dxml.dictionary('entry', package_meta, required=False), nested='supplements')

    format_processor = dxml.dictionary('format', [
        dxml.string('license'),
        dxml.string('vendor'),
        dxml.string('group'),
        dxml.string('buildhost'),
        dxml.string('sourcerpm'),
        header_range_processor,
        provides_processor,
        requires_processor,
        conflicts_processor,
        enhances_processor,
        files_processor,
        obsoletes_processor,
        recommends_processor,
        suggests_processor,
        supplements_processor
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
    """
    Parse comps data and returns it in Python dictionary form
    """
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

    # header_processor data are shared across group, category and environment
    header_processor: list = [
        dxml.string('id'),
        dxml.array(dxml.dictionary('name', [
            dxml.string('.', 'lang', default='en', required=False),
            dxml.string('.', alias='content')
        ], alias='entry'), alias='name'),
        dxml.array(dxml.dictionary('description', [
            dxml.string('.', 'lang', default='en', required=False),
            dxml.string('.', alias='content')
        ], alias='entry'), alias='description')
    ]

    group_child_elem = header_processor.copy()
    group_child_elem.extend([
        dxml.boolean('default'),
        dxml.boolean('uservisible'),
        dxml.dictionary('packagelist', [
            dxml.array(dxml.dictionary('packagereq', [
                dxml.string('.', 'type'),
                dxml.string('.', alias='package_name')
            ]))
        ])
    ])
    group_processor = dxml.array(dxml.dictionary('group', group_child_elem))

    groupid_elem = [dxml.array(dxml.string('groupid'))]
    category_child_elem = header_processor.copy()
    category_child_elem.extend([
        dxml.integer('display_order'),
        dxml.dictionary('grouplist', groupid_elem)
    ])
    category_processor = dxml.array(dxml.dictionary('category', category_child_elem))

    environment_child_elem = header_processor.copy()
    environment_child_elem.extend([
        dxml.integer('display_order'),
        dxml.dictionary('grouplist', groupid_elem),
        dxml.dictionary('optionlist', groupid_elem)
    ])
    environment_processor = dxml.array(dxml.dictionary('environment', environment_child_elem))

    comps_processor = dxml.dictionary('comps', [group_processor, category_processor, environment_processor])
    return dxml.parse_from_file(comps_processor, new_filename)


def parse_primary_new(filename: str):
    """
    Parse primary.xml using new approach of parsing data by database model

    :param filename: The filename for primary.xml
    :returns: A dictionary containing parsed data
    """
    # # Fuck XML.
    # # Also, fuck primary.xml.

    # Alright, new approach, new way, and probably the **best** way to work with XML.
    # Downside of this approach is it is required to parse file repeatedly
    # Maybe I will use the _proper_ way by combining all processor into an array and iterate
    # through the processor array

    # Root dictionary to hold all parsed data.
    root_dictionary = {}

    # Packages database model parsing
    package_processor = dxml.array(dxml.dictionary('package', [
        dxml.string('checksum', alias='pkgId'),
        dxml.string('name'),
        dxml.string('arch'),
        dxml.string('version', 'ver', alias='version'),
        dxml.integer('version', 'epoch', alias='epoch'),
        dxml.string('version', 'rel', alias='release'),
        dxml.string('summary'),
        dxml.string('description'),
        dxml.string('url'),
        dxml.integer('time', 'file', alias='time_file'),
        dxml.integer('time', 'build', alias='time_build'),
        dxml.string('format/license', alias='rpm_license'),
        dxml.string('format/vendor', alias='rpm_vendor'),
        dxml.string('format/group', alias='rpm_group'),
        dxml.string('format/buildhost', alias='rpm_buildhost'),
        dxml.string('format/sourcerpm', alias='rpm_suorcerpm'),
        dxml.integer('format/header-range', 'start', alias='rpm_header_start'),
        dxml.integer('format/header-range', 'end', alias='rpm_header_end'),
        dxml.string('packager', alias='rpm_packager'),
        dxml.integer('size', 'package', alias='size_package'),
        dxml.integer('size', 'installed', alias='size_installed'),
        dxml.integer('size', 'archive', alias='size_archive'),
        dxml.string('location', 'href', alias='location_href'),
        dxml.string('location', 'base', alias='location_base', default=None, required=False),
        dxml.string('checksum', 'type', alias='checksum_type')
    ]), nested='metadata')
    root_dictionary.update({'packages': dxml.parse_from_file(package_processor, filename)})

    # BEGIN copypaste
    conflicts_processor = dxml.array(dxml.dictionary('package', [
        dxml.string('checksum', alias='pkgId'),
        dxml.array(dxml.dictionary('entry', [
            dxml.string('.', 'name'),
            dxml.string('.', 'flags', required=False, default=None),
            dxml.integer('.', 'epoch', required=False, default=None),
            dxml.string('.', 'ver', required=False, alias='version', default=None),
            dxml.string('.', 'rel', required=False, alias='release', default=None)
        ], required=False), nested='format/conflicts', alias='conflicts', omit_empty=True)
    ]), nested='metadata')
    root_dictionary.update({'conflicts': dxml.parse_from_file(conflicts_processor, filename)})

    enhances_processor = dxml.array(dxml.dictionary('package', [
        dxml.string('checksum', alias='pkgId'),
        dxml.array(dxml.dictionary('entry', [
            dxml.string('.', 'name'),
            dxml.string('.', 'flags', required=False, default=None),
            dxml.integer('.', 'epoch', required=False, default=None),
            dxml.string('.', 'ver', required=False, alias='version', default=None),
            dxml.string('.', 'rel', required=False, alias='release', default=None)
        ], required=False), nested='format/enhances', alias='enhances', omit_empty=True)
    ]), nested='metadata')
    root_dictionary.update({'enhances': dxml.parse_from_file(enhances_processor, filename)})

    obsoletes_processor = dxml.array(dxml.dictionary('package', [
        dxml.string('checksum', alias='pkgId'),
        dxml.array(dxml.dictionary('entry', [
            dxml.string('.', 'name'),
            dxml.string('.', 'flags', required=False, default=None),
            dxml.integer('.', 'epoch', required=False, default=None),
            dxml.string('.', 'ver', required=False, alias='version', default=None),
            dxml.string('.', 'rel', required=False, alias='release', default=None)
        ], required=False), nested='format/obsoletes', alias='obsoletes', omit_empty=True)
    ]), nested='metadata')
    root_dictionary.update({'obsoletes': dxml.parse_from_file(obsoletes_processor, filename)})

    provides_processor = dxml.array(dxml.dictionary('package', [
        dxml.string('checksum', alias='pkgId'),
        dxml.array(dxml.dictionary('entry', [
            dxml.string('.', 'name'),
            dxml.string('.', 'flags', required=False, default=None),
            dxml.integer('.', 'epoch', required=False, default=None),
            dxml.string('.', 'ver', required=False, alias='version', default=None),
            dxml.string('.', 'rel', required=False, alias='release', default=None)
        ], required=False), nested='format/provides', alias='provides', omit_empty=True)
    ]), nested='metadata')
    root_dictionary.update({'provides': dxml.parse_from_file(provides_processor, filename)})

    recommends_processor = dxml.array(dxml.dictionary('package', [
        dxml.string('checksum', alias='pkgId'),
        dxml.array(dxml.dictionary('entry', [
            dxml.string('.', 'name'),
            dxml.string('.', 'flags', required=False, default=None),
            dxml.integer('.', 'epoch', required=False, default=None),
            dxml.string('.', 'ver', required=False, alias='version', default=None),
            dxml.string('.', 'rel', required=False, alias='release', default=None)
        ], required=False), nested='format/recommends', alias='recommends', omit_empty=True)
    ]), nested='metadata')
    root_dictionary.update({'recommends': dxml.parse_from_file(recommends_processor, filename)})

    requires_processor = dxml.array(dxml.dictionary('package', [
        dxml.string('checksum', alias='pkgId'),
        dxml.array(dxml.dictionary('entry', [
            dxml.string('.', 'name'),
            dxml.string('.', 'flags', required=False, default=None),
            dxml.integer('.', 'epoch', required=False, default=None),
            dxml.string('.', 'ver', required=False, alias='version', default=None),
            dxml.string('.', 'rel', required=False, alias='release', default=None),
            dxml.integer('.', 'pre', required=False, default=0)
        ], required=False), nested='format/requires', alias='requires', omit_empty=True)
    ]), nested='metadata')
    root_dictionary.update({'requires': dxml.parse_from_file(requires_processor, filename)})

    suggests_processor = dxml.array(dxml.dictionary('package', [
        dxml.string('checksum', alias='pkgId'),
        dxml.array(dxml.dictionary('entry', [
            dxml.string('.', 'name'),
            dxml.string('.', 'flags', required=False, default=None),
            dxml.integer('.', 'epoch', required=False, default=None),
            dxml.string('.', 'ver', required=False, alias='version', default=None),
            dxml.string('.', 'rel', required=False, alias='release', default=None)
        ], required=False), nested='format/suggests', alias='suggests', omit_empty=True)
    ]), nested='metadata')
    root_dictionary.update({'suggests': dxml.parse_from_file(suggests_processor, filename)})

    supplements_processor = dxml.array(dxml.dictionary('package', [
        dxml.string('checksum', alias='pkgId'),
        dxml.array(dxml.dictionary('entry', [
            dxml.string('.', 'name'),
            dxml.string('.', 'flags', required=False, default=None),
            dxml.integer('.', 'epoch', required=False, default=None),
            dxml.string('.', 'ver', required=False, alias='version', default=None),
            dxml.string('.', 'rel', required=False, alias='release', default=None)
        ], required=False), nested='format/supplements', alias='supplements', omit_empty=True)
    ]), nested='metadata')
    root_dictionary.update({'supplements': dxml.parse_from_file(supplements_processor, filename)})
    # END copypaste

    return root_dictionary
