class InvalidState(Exception):
    """Used when repomd data reaches an unexpected state"""
    pass


class UnsupportedFileListException(Exception):
    """Used when the file list version is unsupported"""
    def __init__(self, version):
        super().__init__(f'This file list version is unsupported. Please raise an issue. '
                         f'Currently support version {version} only.')

