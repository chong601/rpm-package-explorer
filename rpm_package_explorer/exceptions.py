# TODO: add/import version support here

class InvalidState(Exception):
    """Used when repomd data reaches an unexpected state"""
    pass


class UnsupportedFileListException(Exception):
    """Used when the file list version is unsupported"""
    def __init__(self, version):
        super().__init__(f'This file list database version is unsupported. Please raise an issue. '
                         f'Currently support version {version} only.')


class UnsupportedPrimaryDatabaseException(Exception):
    """Used when the primary version is unsupported"""
    def __init__(self, version) -> None:
        super().__init__(f'This primary database version is unsupported. Please raise an issue. '
                         f'Currently support version {version} only.')


class UnsupportedOtherDatabaseException(Exception):
    """Used when the other version is unsupported"""
    def __init__(self, version) -> None:
        super().__init__(f'This other database version is unsupported. Please raise an issue. '
                         f'Currently support version {version} only.')
