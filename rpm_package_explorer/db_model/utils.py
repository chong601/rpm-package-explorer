"""
Module that provides various database-related utils mainly for mapping data to and from
database models, as well as formatting data as required.

This util is just a prototype and may significantly change depending on how it will be used.
Or it could be gone, idk.

This shouldn't exist, but:
- I don't want to clutter up model __init__ with data validation (most models here has
  requirements on which data needs to exist)
- Copy-pasting code sucks. Every model needs to call the same code that performs validation
- The need to use if..else to provide the list of required attribute for respective models
  kinda blows for code readability
- Flask-SQLAlchemy has issues with code suggestions when it comes to DB session queries.
"""
import sqlite3
from .sqlalchemy_models import *  # pylint: disable=unused-wildcard-import

# Dictionary that returns the database model class based on what class it's from
DB_MODEL = {
    'db_info': DBInfo,
    'packages': Packages,
    'conflicts': Conflicts,
    'enhances': Enhances,
    'files': Files,
    'obsoletes': Obsoletes,
    'provides': Provides,
    'recommends': Recommends,
    'requires': Requires,
    'suggests': Suggests,
    'supplements': Supplements,
    'filelist': FileList,
    'changelog': ChangeLog
}

# A dictionary that provides the minimum set of attributes that a DB require
DB_REQUIRED_DATA = {
    'db_info': [
        'repo_category',
        'dbversion',
        'checksum'
    ],
    'packages': [
        'pkgId',
        'name',
        'arch',
        'version',
        'epoch',
        'release',
        'summary',
        'description',
        'url',
        'time_file',
        'time_build',
        'rpm_license',
        'rpm_vendor',
        'rpm_group',
        'rpm_buildhost',
        'rpm_sourcerpm',
        'rpm_header_start',
        'rpm_header_end',
        'rpm_packager',
        'size_package',
        'size_installed',
        'size_archive',
        'location_href',
        'location_base',
        'checksum_type'
    ],
    'conflicts': [
        'pkgId',
        'name',
        'flags',
        'epoch',
        'version',
        'release'
    ],
    'enhances': [
        'pkgId',
        'name',
        'flags',
        'epoch',
        'version',
        'release'
    ],
    'files': [
        'pkgId',
        'name',
        'type'
    ],
    'obsoletes': [
        'pkgId',
        'name',
        'flags',
        'epoch',
        'version',
        'release'
    ],
    'provides': [
        'pkgId',
        'name',
        'flags',
        'epoch',
        'version',
        'release'
    ],
    'recommends': [
        'pkgId',
        'name',
        'flags',
        'epoch',
        'version',
        'release'
    ],
    'requires': [
        'pkgId',
        'name',
        'flags',
        'epoch',
        'version',
        'release',
        'pre'
    ],
    'suggests': [
        'pkgId',
        'name',
        'flags',
        'epoch',
        'version',
        'release'
    ],
    'supplements': [
        'pkgId',
        'name',
        'flags',
        'epoch',
        'version',
        'release'
    ],
    'filelist': [
        'pkgId',
        'filename',
        'filetype'
    ],
    'changelog': [
        'pkgId',
        'author',
        'date',
        'changelog'
    ]
}

PRIMARY_DB_QUERY_V10 = {
    'conflicts': 'select p.pkgId, c.name, c.flags, c.epoch, c.version, c.release from conflicts c inner join packages p on p.pkgKey == c.pkgKey',
    'enhances': 'select p.pkgId, e.name, e.flags, e.epoch, e.version, e.release from enhances e inner join packages p on p.pkgKey == e.pkgKey',
    'files': 'select p.pkgId, f.name, f.type from files f inner join packages p on p.pkgKey == f.pkgKey',
    'obsoletes': 'select p.pkgId, o.name, o.flags, o.epoch, o.version, o.release from obsoletes o inner join packages p on p.pkgKey == o.pkgKey',
    'packages': 'select * from packages',
    'provides': 'select p.pkgId, pr.name, pr.flags, pr.epoch, pr.version, pr.release from provides pr inner join packages p on p.pkgKey == pr.pkgKey',
    'recommends': 'select p.pkgId, r.name, r.flags, r.epoch, r.version, r.release from recommends r inner join packages p on p.pkgKey == r.pkgKey',
    'requires': 'select p.pkgId, r.name, r.flags, r.epoch, r.version, r.release, r.pre from requires r inner join packages p on p.pkgKey == r.pkgKey',
    'suggests': 'select p.pkgId, s.name, s.flags, s.epoch, s.version, s.release from suggests s inner join packages p on p.pkgKey == s.pkgKey',
    'supplements': 'select p.pkgId, s.name, s.flags, s.epoch, s.version, s.release from supplements s inner join packages p on p.pkgKey == s.pkgKey'
}

FILELISTS_DB_QUERY_V10 = {
    'filelist': None
}

OTHER_DB_QUERY_V10 = {
    'changelog': None
}

PRIMARY_DB_VERSION = {
    10: PRIMARY_DB_QUERY_V10
}

FILELISTS_DB_VERSION = {
    10: FILELISTS_DB_QUERY_V10
}

OTHER_DB_VERSION = {
    10: OTHER_DB_QUERY_V10
}


class DBModelFactory(object):
    """Factory class that provide """

    def __init__(self, table_name, data=None) -> None:
        self._table_name = table_name
        self.db_model = None
        if data is not None:
            self.add_data(data)

    def _check_missing(self, data):
        required_attr = DB_REQUIRED_DATA.get(self._table_name)
        missing_attr = [attr for attr in required_attr if attr not in data]

        if missing_attr:
            raise AttributeError(f'Missing required attribute for '
                                 f'{DB_MODEL.get(self._table_name).__class__.__name__}: {missing_attr}')

    def add_data(self, data: dict, force_overwrite=False):
        self._check_missing(data)
        db_model = DB_MODEL.get(self._table_name)
        self.db_model = db_model(**data)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.db_model})'


def map_row_to_dict(cursor: sqlite3.Cursor, row_data):
    """
    Just a neat function that converts cursor tuple-y data into dictionary
    Used by SQLite module to map results into a dictionary

    :param cursor: The cursor after a query is executed
    :param row_data: The row data after the query is executed
    :returns: A dictionary of the query data in the form of {column_name: row_data}
    """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row_data[idx]
    return d


def SQLiteDataExtraction():
    pass
