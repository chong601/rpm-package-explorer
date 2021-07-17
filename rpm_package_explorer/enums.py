import enum


class State(enum.Enum):
    """State enums for repomd data parsing state"""
    STARTED = 0
    VERSION = 1
    FILE_LIST = 2
    CHECKSUMS = 3
    END = 4
