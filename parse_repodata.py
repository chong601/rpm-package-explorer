import os

from rpm_package_explorer.xmlparser import parse_repomd
from rpm_package_explorer.utils import open_file
from rpm_package_explorer.io_handler import read_data

# Create workdir before begin processing data
WORKDIR = 'workdir'
SUPPORTED_DATABASE_VERSIONS = [10]
PARSE_DATA = ['primary', 'filelists', 'other', 'primary_db', 'filelists_db', 'other_db', 'group', 'group_gz',
              'updateinfo']
# Set up directories
real_workdir = os.path.join(os.getcwd(), WORKDIR)
if not os.path.isdir(real_workdir):
    os.mkdir(real_workdir)

real_repo_data = os.path.join(os.getcwd())
if not os.path.isdir(real_repo_data):
    os.mkdir(real_repo_data)

# Parse repomd.xml data
repomd_data = parse_repomd('repodata/repomd.xml')

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
    print(source_filename, dest_filename)

# Clean up workdir


