import uuid
from dataclasses import dataclass
from sqlalchemy import Text, Integer, Boolean, Column, TIMESTAMP


@dataclass
class DBInfo(object):
    __tablename__ = 'db_info'

    dbinfo_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    repo_category = Column(Text, comment='Repository category that this row represents')
    dbversion = Column(Integer, comment='DB version')
    checksum = Column(Text, comment='Hash for the XML file')

    @staticmethod
    def _get_required_columns():
        return ['repo_category',
                'dbversion',
                'checksum']

    def __init__(self, **kwargs):
        # FUUUUUUUUUUUCK
        if len(kwargs) == 0:
            raise AttributeError(f'{self.__class__.__name__} object requires the following keywords available: '
                                 f'{", ".join(self._get_required_columns())}')
        else:
            missing_attr = []
            for attr in self._get_required_columns():
                if attr not in kwargs:
                    missing_attr.append(attr)

            if len(missing_attr) > 0:
                raise AttributeError(f'Required attributes are missing: {", ".join(missing_attr)}')
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass
class Packages(object):
    """Represents the `packages` table"""
    __tablename__ = 'packages'

    pkg_uuid: str = Column(Text, primary_key=True, default=uuid.uuid4)
    pkgKey: int = Column(Integer, primary_key=True, comment='Primary key for the packages')
    # Also used as a package hash
    pkgId: str = Column(Text, nullable=False, comment='The package ID of the package')
    name: str = Column(Text, nullable=False, comment='Package name')
    arch: str = Column(Text, nullable=False, comment='Architecture the package is for')
    version: str = Column(Text, nullable=False, comment='Package version')
    epoch: int = Column(Integer, nullable=False, comment='Package epoch')
    release: str = Column(Text, nullable=False, comment='Package release')
    summary: str = Column(Text, nullable=False, comment='Package summary')
    description: str = Column(Text, nullable=False, comment='Package description')
    url: str = Column(Text, comment='Package upstream URL')
    time_file: int = Column(TIMESTAMP, comment='File timestamp')
    time_build: int = Column(TIMESTAMP, comment='File build time')
    rpm_license: str = Column(Text, comment='Package license')
    rpm_vendor: str = Column(Text)
    rpm_group: str = Column(Text)
    rpm_buildhost: str = Column(Text)
    rpm_sourcerpm: str = Column(Text, comment='Source RPM file location')
    rpm_header_start: int = Column(Integer)
    rpm_header_end: int = Column(Integer)
    rpm_packager: str = Column(Text)
    size_package: int = Column(Integer)
    size_installed: int = Column(Integer)
    size_archive: int = Column(Integer)
    location_href: str = Column(Text)
    location_base: str = Column(Text)
    checksum_type: str = Column(Text)

    @staticmethod
    def _get_required_columns():
        """Returns the required columns for this table"""
        return ['pkgKey',
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
                'checksum_type']

    def __init__(self, **kwargs):
        """Initialize package object based on the passed in keyword arguments

        :param **kwargs: Keyword arguments containing package data to be inserted into the database
        """
        # FUUUUUUUUUUUCK
        if len(kwargs) == 0:
            raise AttributeError(f'{self.__class__.__name__} object requires the following keywords available: '
                                 f'{", ".join(self._get_required_columns())}')
        else:
            missing_attr = []
            for attr in self._get_required_columns():
                if attr not in kwargs:
                    missing_attr.append(attr)

            if len(missing_attr) > 0:
                raise AttributeError(f'Required attributes are missing: {", ".join(missing_attr)}')
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass
class Conflicts(object):
    __tablename__ = 'conflicts'

    conflict_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    pkgKey = Column(Integer)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package conflict comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package conflicts with')
    version = Column(Integer, comment='Package version that the package conflicts with')
    release = Column(Integer, comment='Package release that the package conflicts with')

    @staticmethod
    def _get_required_columns():
        return ['pkgKey',
                'name',
                'flags',
                'epoch',
                'version',
                'release']

    def __init__(self, **kwargs):
        # FUUUUUUUUUUUCK
        if len(kwargs) == 0:
            raise AttributeError(f'{self.__class__.__name__} object requires the following keywords available: '
                                 f'{", ".join(self._get_required_columns())}')
        else:
            missing_attr = []
            for attr in self._get_required_columns():
                if attr not in kwargs:
                    missing_attr.append(attr)

            if len(missing_attr) > 0:
                raise AttributeError(f'Required attributes are missing: {", ".join(missing_attr)}')
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass
class Enhances(object):
    __tablename__ = 'enhances'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    pkgKey = Column(Integer)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package conflict comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package enhances')
    version = Column(Integer, comment='Package version that the package enhances')
    release = Column(Integer, comment='Package release that the package enhances')

    @staticmethod
    def _get_required_columns():
        return ['pkgKey',
                'name',
                'flags',
                'epoch',
                'version',
                'release']

    def __init__(self, **kwargs):
        # FUUUUUUUUUUUCK
        if len(kwargs) == 0:
            raise AttributeError(f'{self.__class__.__name__} object requires the following keywords available: '
                                 f'{", ".join(self._get_required_columns())}')
        else:
            missing_attr = []
            for attr in self._get_required_columns():
                if attr not in kwargs:
                    missing_attr.append(attr)

            if len(missing_attr) > 0:
                raise AttributeError(f'Required attributes are missing: {", ".join(missing_attr)}')
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass
class Files(object):
    """Class that represents the files table

    Note: This table will follow the saner approach of listing each file in its own row
    rather than the original format that uses / as the separator for the file name and
    per-character separator for file type in the original SQLite packages database
    """
    __tablename__ = 'files'

    file_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    pkgKey = Column(Integer)
    name = Column(Text, comment='File name')
    type = Column(Text, comment='File type')

    @staticmethod
    def _get_required_columns():
        return ['pkgKey',
                'name',
                'type']

    def __init__(self, **kwargs):
        # FUUUUUUUUUUUCK
        if len(kwargs) == 0:
            raise AttributeError(f'{self.__class__.__name__} object requires the following keywords available: '
                                 f'{", ".join(self._get_required_columns())}')
        else:
            missing_attr = []
            for attr in self._get_required_columns():
                if attr not in kwargs:
                    missing_attr.append(attr)

            if len(missing_attr) > 0:
                raise AttributeError(f'Required attributes are missing: {", ".join(missing_attr)}')
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass
class Obsoletes(object):
    __tablename__ = 'obsoletes'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    pkgKey = Column(Integer)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package obsolete comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package obsoletes')
    version = Column(Integer, comment='Package version that the package obsoletes')
    release = Column(Integer, comment='Package release that the package obsoletes')

    @staticmethod
    def _get_required_columns():
        return ['pkgKey',
                'name',
                'flags',
                'epoch',
                'version',
                'release']

    def __init__(self, **kwargs):
        # FUUUUUUUUUUUCK
        if len(kwargs) == 0:
            raise AttributeError(f'{self.__class__.__name__} object requires the following keywords available: '
                                 f'{", ".join(self._get_required_columns())}')
        else:
            missing_attr = []
            for attr in self._get_required_columns():
                if attr not in kwargs:
                    missing_attr.append(attr)

            if len(missing_attr) > 0:
                raise AttributeError(f'Required attributes are missing: {", ".join(missing_attr)}')
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass()
class Provides(object):
    __tablename__ = 'provides'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    pkgKey = Column(Integer)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package obsolete comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package provides')
    version = Column(Integer, comment='Package version that the package provides')
    release = Column(Integer, comment='Package release that the package provides')

    @staticmethod
    def _get_required_columns():
        return ['pkgKey',
                'name',
                'flags',
                'epoch',
                'version',
                'release']

    def __init__(self, **kwargs):
        # FUUUUUUUUUUUCK
        if len(kwargs) == 0:
            raise AttributeError(f'{self.__class__.__name__} object requires the following keywords available: '
                                 f'{", ".join(self._get_required_columns())}')
        else:
            missing_attr = []
            for attr in self._get_required_columns():
                if attr not in kwargs:
                    missing_attr.append(attr)

            if len(missing_attr) > 0:
                raise AttributeError(f'Required attributes are missing: {", ".join(missing_attr)}')
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass
class Recommends(object):
    __tablename__ = 'Recommends'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    pkgKey = Column(Integer)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package obsolete comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package provides')
    version = Column(Integer, comment='Package version that the package provides')
    release = Column(Integer, comment='Package release that the package provides')

    @staticmethod
    def _get_required_columns():
        return ['pkgKey',
                'name',
                'flags',
                'epoch',
                'version',
                'release']

    def __init__(self, **kwargs):
        # FUUUUUUUUUUUCK
        if len(kwargs) == 0:
            raise AttributeError(f'{self.__class__.__name__} object requires the following keywords available: '
                                 f'{", ".join(self._get_required_columns())}')
        else:
            missing_attr = []
            for attr in self._get_required_columns():
                if attr not in kwargs:
                    missing_attr.append(attr)

            if len(missing_attr) > 0:
                raise AttributeError(f'Required attributes are missing: {", ".join(missing_attr)}')
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass
class Requires(object):
    __tablename__ = 'requires'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    pkgKey = Column(Integer)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package obsolete comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package provides')
    version = Column(Integer, comment='Package version that the package provides')
    release = Column(Integer, comment='Package release that the package provides')
    pre = Column(Boolean, comment='Signals if the requirement is a prerequisite for preinstallation')

    @staticmethod
    def _get_required_columns():
        return ['pkgKey',
                'name',
                'flags',
                'epoch',
                'version',
                'release',
                'pre']

    def __init__(self, **kwargs):
        # FUUUUUUUUUUUCK
        if len(kwargs) == 0:
            raise AttributeError(f'{self.__class__.__name__} object requires the following keywords available: '
                                 f'{", ".join(self._get_required_columns())}')
        else:
            missing_attr = []
            for attr in self._get_required_columns():
                if attr not in kwargs:
                    missing_attr.append(attr)

            if len(missing_attr) > 0:
                raise AttributeError(f'Required attributes are missing: {", ".join(missing_attr)}')
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass
class Suggests(object):
    __tablename__ = 'Suggests'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    pkgKey = Column(Integer)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package obsolete comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package provides')
    version = Column(Integer, comment='Package version that the package provides')
    release = Column(Integer, comment='Package release that the package provides')

    @staticmethod
    def _get_required_columns():
        return ['pkgKey',
                'name',
                'flags',
                'epoch',
                'version',
                'release']

    def __init__(self, **kwargs):
        # FUUUUUUUUUUUCK
        if len(kwargs) == 0:
            raise AttributeError(f'{self.__class__.__name__} object requires the following keywords available: '
                                 f'{", ".join(self._get_required_columns())}')
        else:
            missing_attr = []
            for attr in self._get_required_columns():
                if attr not in kwargs:
                    missing_attr.append(attr)

            if len(missing_attr) > 0:
                raise AttributeError(f'Required attributes are missing: {", ".join(missing_attr)}')
        for k, v in kwargs.items():
            setattr(self, k, v)


@dataclass
class Supplements(object):
    __tablename__ = 'supplements'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    pkgKey = Column(Integer)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package obsolete comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package provides')
    version = Column(Integer, comment='Package version that the package provides')
    release = Column(Integer, comment='Package release that the package provides')

    @staticmethod
    def _get_required_columns():
        return ['pkgKey',
                'name',
                'flags',
                'epoch',
                'version',
                'release']

    def __init__(self, **kwargs):
        # FUUUUUUUUUUUCK
        if len(kwargs) == 0:
            raise AttributeError(f'{self.__class__.__name__} object requires the following keywords available: '
                                 f'{", ".join(self._get_required_columns())}')
        else:
            missing_attr = []
            for attr in self._get_required_columns():
                if attr not in kwargs:
                    missing_attr.append(attr)

            if len(missing_attr) > 0:
                raise AttributeError(f'Required attributes are missing: {", ".join(missing_attr)}')
        for k, v in kwargs.items():
            setattr(self, k, v)
