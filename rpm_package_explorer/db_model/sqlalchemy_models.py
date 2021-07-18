from sqlalchemy import Text, Integer, Boolean, Column, TIMESTAMP
import uuid


class Packages():
    __tablename__ = 'packages'
    pkg_uuid = Column(Text, primary_key=True, autoincrement=True, default=uuid.uuid4)
    pkgKey = Column(Integer, autoincrement=False, primary_key=True, comment='Primary key for the packages')
    pkgId = Column(Text, nullable=False, comment='The package ID of the package')
    name = Column(Text, nullable=False, comment='Package name')
    arch = Column(Text, nullable=False, comment='Architecture the package is for')
    version = Column(Text, nullable=False, comment='Package version')
    epoch = Column(Integer, nullable=False, comment='Package epoch')
    release = Column(Text, nullable=False, comment='Package release')
    summary = Column(Text, nullable=False, comment='Package summary')
    description = Column(Text, nullable=False, comment='Package description')
    url = Column(Text, comment='Package upstream URL')
    time_file = Column(TIMESTAMP, comment='File timestamp')
    time_build = Column(TIMESTAMP, comment='File build time')
    rpm_license = Column(Text, comment='Package license')
    rpm_vendor = Column(Text)
    rpm_group = Column(Text)
    rpm_buildhost = Column(Text)
    rpm_sourcerpm = Column(Text, comment='Source RPM file location')
    rpm_header_start = Column(Integer)
    rpm_header_end = Column(Integer)
    rpm_packager = Column(Text)
    size_package = Column(Integer)
    size_installed = Column(Integer)
    size_archive = Column(Integer)
    location_href = Column(Text)
    location_base = Column(Text)
    checksum_type = Column(Text)


class Conflicts():
    __tablename__ = 'conflicts'

    conflict_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package conflict comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package conflicts with')
    version = Column(Integer, comment='Package version that the package conflicts with')
    release = Column(Integer, comment='Package release that the package conflicts with')
    pkgKey = Column(Integer)


class Enhances():
    __tablename__ = 'enhances'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package conflict comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package enhances')
    version = Column(Integer, comment='Package version that the package enhances')
    release = Column(Integer, comment='Package release that the package enhances')
    pkgKey = Column(Integer)


class Files():
    """Class that represents the files table

    Note: This table will follow the saner approach of listing each file in its own row
    rather than the original format that uses / as the separator for the file name and
    per-character separator for file type in the original SQLite packages database
    """
    __tablename__ = 'files'

    file_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    name = Column(Text, comment='File name')
    type = Column(Text, comment='File type')
    pkgKey = Column(Integer)


class Obsoletes():
    __tablename__ = 'obsoletes'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package obsolete comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package obsoletes')
    version = Column(Integer, comment='Package version that the package obsoletes')
    release = Column(Integer, comment='Package release that the package obsoletes')
    pkgKey = Column(Integer)


class Provides():
    __tablename__ = 'provides'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package obsolete comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package provides')
    version = Column(Integer, comment='Package version that the package provides')
    release = Column(Integer, comment='Package release that the package provides')
    pkgKey = Column(Integer)


class Recommends():
    __tablename__ = 'Recommends'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package obsolete comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package provides')
    version = Column(Integer, comment='Package version that the package provides')
    release = Column(Integer, comment='Package release that the package provides')
    pkgKey = Column(Integer)


class Requires():
    __tablename__ = 'requires'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package obsolete comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package provides')
    version = Column(Integer, comment='Package version that the package provides')
    release = Column(Integer, comment='Package release that the package provides')
    pkgKey = Column(Integer)
    pre = Column(Boolean, comment='Signals if the requirement is a prerequisite for preinstallation')


class Suggests():
    __tablename__ = 'Suggests'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package obsolete comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package provides')
    version = Column(Integer, comment='Package version that the package provides')
    release = Column(Integer, comment='Package release that the package provides')
    pkgKey = Column(Integer)


class Supplements():
    __tablename__ = 'supplements'

    enhance_uuid = Column(Text, primary_key=True, default=uuid.uuid4)
    name = Column(Text, comment='Package name')
    flags = Column(Text, comment='Package obsolete comparison flag')
    epoch = Column(Integer, comment='Package epoch that the package provides')
    version = Column(Integer, comment='Package version that the package provides')
    release = Column(Integer, comment='Package release that the package provides')
    pkgKey = Column(Integer)
