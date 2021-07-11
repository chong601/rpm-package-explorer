class InvalidState(Exception):
    pass


class UnsupportedFileListException(Exception):
    def __init__(self, version):
        super().__init__(f'This file list version is unsupported. Please raise an issue. '
                         f'Currently support version {version} only.')

