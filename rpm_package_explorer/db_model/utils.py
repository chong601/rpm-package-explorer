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

from .sqlalchemy_models import *

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
    DBInfo: ['repo_category',
             'dbversion',
             'checksum'],
    Packages: ['pkgKey',
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
               'checksum_type'],
    Conflicts: ['pkgKey',
                'name',
                'flags',
                'epoch',
                'version',
                'release'],
    Enhances: ['pkgKey',
               'name',
               'flags',
               'epoch',
               'version',
               'release'],
    Files: ['pkgKey',
            'name',
            'type'],
    Obsoletes: ['pkgKey',
                'name',
                'flags',
                'epoch',
                'version',
                'release'],
    Provides: ['pkgKey',
               'name',
               'flags',
               'epoch',
               'version',
               'release'],
    Recommends: ['pkgKey',
                 'name',
                 'flags',
                 'epoch',
                 'version',
                 'release'],
    Requires: ['pkgKey',
               'name',
               'flags',
               'epoch',
               'version',
               'release',
               'pre'],
    Suggests: ['pkgKey',
               'name',
               'flags',
               'epoch',
               'version',
               'release'],
    Supplements: ['pkgKey',
                  'name',
                  'flags',
                  'epoch',
                  'version',
                  'release'],
    FileList: ['pkgKey',
               'dirname',
               'filenames',
               'filetypes'],
    ChangeLog: ['pkgKey',
                'date',
                'changelog']
}


class DBModelFactory(object):
    """Factory class that provide """
    def __init__(self, db_model, data=None) -> None:
        self.db_model: object = db_model
        if data is not None:
            self.add_data(data)

    def _check_missing(self, data):
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


        if len(existing_attr) > 0:
            required_attr = [new_attr for new_attr in required_attr if existing_attr in required_attr]

        missing_attr = [attr for attr in required_attr if attr not in required_attr]

        if missing_attr:
            raise AttributeError(f'Missing attribute for {self.db_model.__class__.__name__}: {missing_attr}')

    def add_data(self, data, force_overwrite=False):
        self._check_missing(data)
        existing_attr = vars(self.db_model)
        for k, v in data:
            if k in existing_attr and not force_overwrite:
                continue
            setattr(self.db_model, k, v)

