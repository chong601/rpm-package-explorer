import hashlib
import logging
import re

from rpm_package_explorer.enums import State
from rpm_package_explorer.exceptions import InvalidState, UnsupportedFileListException
from rpm_package_explorer.io_handler import read_data
from rpm_package_explorer.utils import open_file

SUPPORTED_FILETIMELIST_VERSIONS = [2]
SUPPORTED_DB_VERSIONS = [10]

# Dict for state mapping
# **Could** use finite-state-engine, but that's a comp-sci hellhole that I'm not ready to get into it.
# This will do, as long there's no major changes.
state_map = {
    State.STARTED: State.VERSION,
    State.VERSION: State.FILE_LIST,
    State.FILE_LIST: State.CHECKSUMS,
    State.CHECKSUMS: State.END
}

if __name__ == '__main__':
    repodata = {}
    extensions = {}

    with open('repo_data/fullfiletimelist-rocky', encoding='utf8') as fullfiletimelist:
        # Divide state into 4
        # 0 when started
        # 1 when data version is parsed
        # 2 when file list is parsed
        # 3 when checksums data are read
        state = State.STARTED
        count = 0

        for data in fullfiletimelist.readlines():
            count += 1
            # Strip all leading and trailling whitespaces
            data = data.strip()
            if data == '':
                continue
            # This thing broke me. At least now it Works On My Machine™
            match = re.match(
                # version
                r'(?P<version>\d+)$|'
                # filelist
                r'(?P<epoch>\d+)\t(?P<type>[ldf])\t(?P<size>\d+)\t(?P<path>[\w+~/.-]+)$|'
                # repomd
                r'(?P<repo_hash>\w+)\t(?P<repo_path>[\w+/.-]+)$|'
                # headers
                r'\[(?P<header>Version|Files|Checksums (?P<hash>\w+)|End)]$',
                data)
            re_match = match.groupdict()
            if re_match.get('header') is not None:
                header_section = re_match.get('header')
                if header_section.find('Version') == 0:
                    if state == State.STARTED:
                        state = state_map.get(state)
                        continue
                elif header_section.find('Files') == 0:
                    if state == State.VERSION:
                        state = state_map.get(state)
                        continue
                elif header_section.find('Checksum') == 0:
                    if state == State.FILE_LIST:
                        state = state_map.get(state)
                        checksum_data = re_match['hash']
                        if checksum_data.lower() == 'sha1':
                            hf = hashlib.sha1()
                        else:
                            logging.warning(f'Detected hash type {checksum_data.lower()}. Please raise a bug issue.')

                        continue
                elif header_section.find('End') == 0:
                    break
            # print(state)
            try:
                if state == State.VERSION:
                    # do version check
                    if int(re_match['version']) not in SUPPORTED_FILETIMELIST_VERSIONS:
                        raise UnsupportedFileListException(SUPPORTED_FILETIMELIST_VERSIONS)
                    # print(re_match)

                elif state == State.FILE_LIST:
                    # Ignore link and directories
                    if re_match['path'].find('repodata') != -1 and re_match['type'] == 'f':
                        with open_file(re_match['path']) as file:
                            for db_data in read_data(file):
                                hf.update(db_data)
                            file_hash = hf.hexdigest()
                    pass
                elif state == State.CHECKSUMS:
                    # process checksum data
                    checksums = {}
                    checksums.update({re_match['repo_path']: re_match['repo_hash']})
                    for repo_path, repo_hash in list(checksums.items()):
                        print(repo_path, repo_hash)

            except Exception as e:
                print(f'Task aborted because of {e}')
