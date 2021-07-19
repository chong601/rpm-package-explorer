import os
import sqlite3
import shutil

from contextlib import closing
from rpm_package_explorer.xmlparser import parse_groups, parse_repomd, parse_primary, parse_filelists, \
                                           parse_otherdata, parse_updateinfo, rearrange_data
from rpm_package_explorer.utils import open_file, map_row_to_dict
from rpm_package_explorer.io_handler import read_data
from rpm_package_explorer.db_model.sqlalchemy_models import *

# Create workdir before begin processing data
WORKDIR = 'workdir'
SUPPORTED_DATABASE_VERSIONS = [10]
# Define which to read first

PARSE_DATA = ['primary_db', 'filelists_db', 'other_db', 'primary', 'filelists', 'other', 'group',
              'group_gz', 'updateinfo']

SKIP_PARSE = ['primary_db', 'other_db', 'filelists_db']

PRIORITY = {
    'primary': ['primary_db', 'primary'],
    'filelists': ['filelists_db', 'filelists'],
    'other': ['other_db', 'other'],
    'group': ['group', 'group_gz'],
    'updateinfo': ['updateinfo']
}

parse_data = [x for x in PARSE_DATA if x not in SKIP_PARSE]

# Set up directories
real_workdir = os.path.join(os.getcwd(), WORKDIR)
if os.path.isdir(real_workdir):
    shutil.rmtree(real_workdir)
os.mkdir(real_workdir)

real_repo_data = os.path.join(os.getcwd())

# Parse repomd.xml data
repomd_data = parse_repomd('repodata/repomd.xml')

# Start filtering data
for priority_list in PRIORITY.values():
    found = False
    for p in priority_list:
        if p in SKIP_PARSE:
            repomd_data.pop(p)
        elif p in parse_data and not found:
            found = True
            continue
        else:
            repomd_data.pop(p)
            parse_data.remove(p)

processed_data = {}

# Start processing files listed in repomd.xml
for repo_type in parse_data:
    # Do quick and dirty data detection
    # TODO: trim this to a one-liner
    data = repomd_data.get(repo_type)
    if 'open_checksum_hash_type' in data and \
       'open_checksum_hash' in data and \
       'open_size' in data:
        is_archive = True
    else:
        is_archive = False
    # TODO: trim this to a one-liner
    if 'database_version' in data:
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
    del data['href']
    data['source_filepath'] = source_filepath
    data['dest_filepath'] = dest_filepath
    processed_data.update({repo_type: data})
# Finish processing repomd.xml

# Start processing data based on processed_data variable
try:
    for repo_category, data in processed_data.items():
        if repo_category == 'primary_db':
            # SQLite doesn't close the "normal" way, so it needs slightly insane way to really close connection.
            with closing(sqlite3.connect(data['dest_filepath'])) as connection, connection, closing(connection.cursor()) as cursor:
                tables = [x[0] for x in cursor.execute(
                    "select tbl_name from sqlite_master where type='table'").fetchall()]
                for table in tables:
                    cursor.execute(f'select * from {table}')
                    # TODO: process data
                    cursor.row_factory = map_row_to_dict
                    for row in cursor.fetchall():
                        row: dict
                        if table == 'db_info':
                            row['repo_category'] = repo_category
                            db_object = DBInfo(**row)
                        elif table == 'packages':
                            db_object = Packages(**row)
                        elif table == 'conflicts':
                            db_object = Conflicts(**row)
                        elif table == 'enhances':
                            db_object = Enhances(**row)
                        elif table == 'files':
                            db_object = Files(**row)
                        elif table == 'obsoletes':
                            db_object = Obsoletes(**row)
                        elif table == 'provides':
                            db_object = Provides(**row)
                        elif table == 'recommends':
                            db_object = Recommends(**row)
                        elif table == 'requires':
                            db_object = Requires(**row)
                        elif table == 'suggests':
                            db_object = Suggests(**row)
                        elif table == 'supplements':
                            db_object = Supplements(**row)
                        print(f"{repo_category} has {db_object}")
        elif repo_category == 'primary':
            extracted_data = parse_primary(data['dest_filepath'])
            for d in extracted_data.values():
                print(f'{repo_category} has {d}')
        elif repo_category == 'filelists_db':
            # SQLite doesn't close the "normal" way, so it needs slightly insane way to really close connection.
            with closing(sqlite3.connect(data['dest_filepath'])) as connection, connection, closing(connection.cursor()) as cursor:
                cursor = connection.cursor()
                tables = [x[0] for x in cursor.execute(
                    "select tbl_name from sqlite_master where type='table'").fetchall()]
                # We don't need to process packages table
                tables.remove('packages')
                for table in tables:
                    cursor.execute(f'select * from {table}')
                    # TODO: process data
                    cursor.row_factory = map_row_to_dict
                    for row in cursor.fetchall():
                        if table == 'db_info':
                            row['repo_category'] = repo_category
                            db_object = DBInfo(**row)
                        elif table == 'filelist':
                            db_object = FileList(**row)
                        print(f'{repo_category} has {db_object}')
        elif repo_category == 'filelists':
            extracted_data = parse_filelists(data['dest_filepath'])
            for d in extracted_data.values():
                print(f'{repo_category} has {d}')
        elif repo_category == 'other_db':
            # SQLite doesn't close the "normal" way, so it needs slightly insane way to really close connection.
            with closing(sqlite3.connect(data['dest_filepath'])) as connection, connection, closing(connection.cursor()) as cursor:
                cursor = connection.cursor()
                tables = [x[0] for x in cursor.execute(
                    "select tbl_name from sqlite_master where type='table'").fetchall()]
                # We don't need to process packages table
                tables.remove('packages')
                for table in tables:
                    cursor.execute(f'select * from {table}')
                    # TODO: process data
                    cursor.row_factory = map_row_to_dict
                    for row in cursor.fetchall():
                        if table == 'db_info':
                            row['repo_category'] = repo_category
                            db_object = DBInfo(**row)
                        elif table == 'filelist':
                            db_object = ChangeLog(**row)
                        print(f'{repo_category} has {db_object}')
        elif repo_category == 'other':
            extracted_data = parse_otherdata(data['dest_filepath'])
            for d in extracted_data.values():
                print(f'{repo_category} has {d}')
        elif repo_category == 'group' or repo_category == 'group_gz':
            extracted_data = parse_groups(data['dest_filepath'])
            for d in extracted_data.values():
                print(f'{repo_category} has {d}')
        elif repo_category == 'updateinfo':
            extracted_data = parse_updateinfo(data['dest_filepath'])
            for d in extracted_data.values():
                print(f'{repo_category} has {d}')
        else:
            print(f'No handler for {repo_category} available. Please raise an issue')
except Exception as e:
    print(e)
# Clean up workdir

shutil.rmtree(real_workdir)
