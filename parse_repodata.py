import os
import sqlite3

from contextlib import closing
from rpm_package_explorer.xmlparser import parse_repomd
from rpm_package_explorer.utils import open_file, map_row_to_dict
from rpm_package_explorer.io_handler import read_data

# Create workdir before begin processing data
WORKDIR = 'workdir'
SUPPORTED_DATABASE_VERSIONS = [10]
# Define which to read first

PARSE_DATA = ['primary', 'filelists', 'other', 'primary_db', 'filelists_db', 'other_db', 'group',
              'group_gz', 'updateinfo']

PRIORITY = {
    'primary': ['primary_db', 'primary'],
    'filelists': ['filelists_db', 'filelists'],
    'other': ['other_db', 'other'],
    'group': ['group', 'group_gz'],
    'updateinfo': ['updateinfo']
}

# Set up directories
real_workdir = os.path.join(os.getcwd(), WORKDIR)
if not os.path.isdir(real_workdir):
    os.mkdir(real_workdir)

real_repo_data = os.path.join(os.getcwd())

# Parse repomd.xml data
repomd_data = parse_repomd('repodata/repomd.xml')

# Start filtering data
all_repo_type = repomd_data.keys()
for priority_list in PRIORITY.values():
    found = False
    for p in priority_list:
        if p in all_repo_type and not found:
            found = True
            continue
        else:
            PARSE_DATA.remove(p)

processed_data = {}

# Start processing files listed in repomd.xml
for repo_type, data in repomd_data.items():
    # Do quick and dirty data detection
    # TODO: trim this to a one-liner
    if data['open_checksum_hash_type'] is not None and \
            data['open_checksum_hash'] is not None and \
            data['open_size'] is not None:
        is_archive = True
    else:
        is_archive = False
    # TODO: trim this to a one-liner
    if data['database_version'] is not None:
        is_db = False
        if data['database_version'] in SUPPORTED_DATABASE_VERSIONS:
            is_db = True
    else:
        is_db = False

    if is_archive:
        source_filename: str = data['href']
        dest_filename = source_filename.rsplit('.', maxsplit=1)[0].replace('repodata/', '')
    else:
        source_filename: str = data['href']
        dest_filename = source_filename.replace('repodata/', '')

    source_filepath = os.path.join(real_repo_data, source_filename)
    dest_filepath = os.path.join(real_workdir, dest_filename)
    if os.path.exists(dest_filepath):
        continue
    with open_file(source_filepath, 'rb') as source_data,\
         open_file(dest_filepath, 'wb') as dest_data:
        for binary_data in read_data(source_data):
            dest_data.write(binary_data)
        dest_data.flush()
    processed_data.update({repo_type: dest_filepath})
# Finish processing repomd.xml

# Start processing data based on processed_data variable
try:
    for repo_category, filename in processed_data.items():
        if repo_category == 'primary_db':
            # SQLite doesn't close the "normal" way, so it needs slightly insane way to really close connection.
            with closing(sqlite3.connect(filename)) as connection, connection, closing(connection.cursor()) as cursor:
                tables = [x[0] for x in cursor.execute(
                    "select tbl_name from sqlite_master where type='table'").fetchall()]
                for table in tables:
                    cursor.execute(f'select * from {table}')
                    # TODO: process data
                    cursor.row_factory
                    for row in cursor.fetchall():
                        print(f'{repo_category} has {map_row_to_dict(cursor, row)}')
        elif repo_category == 'primary':
            pass
        elif repo_category == 'filelists_db':
            # SQLite doesn't close the "normal" way, so it needs slightly insane way to really close connection.
            with closing(sqlite3.connect(filename)) as connection, connection, closing(connection.cursor()) as cursor:
                cursor = connection.cursor()
                tables = [x[0] for x in cursor.execute(
                    "select tbl_name from sqlite_master where type='table'").fetchall()]
                for table in tables:
                    cursor.execute(f'select * from {table}')
                    # TODO: process data
                    for row in cursor.fetchall():
                        print(f'{repo_category} has {map_row_to_dict(cursor, row)}')
        elif repo_category == 'filelists':
            pass
        elif repo_category == 'other_db':
            # SQLite doesn't close the "normal" way, so it needs slightly insane way to really close connection.
            with closing(sqlite3.connect(filename)) as connection, connection, closing(connection.cursor()) as cursor:
                cursor = connection.cursor()
                tables = [x[0] for x in cursor.execute(
                    "select tbl_name from sqlite_master where type='table'").fetchall()]
                for table in tables:
                    cursor.execute(f'select * from {table}')
                    # TODO: process data
                    for row in cursor.fetchall():
                        print(f'{repo_category} has {map_row_to_dict(cursor, row)}')
        elif repo_category == 'other':
            pass
        elif repo_category == 'group' or repo_category == 'group_gz':
            pass
        elif repo_category == 'updateinfo':
            pass
        else:
            print(f'Unable to process {repo_category}. Please raise an issue')
except Exception as e:
    print(e)
# Clean up workdir


