# Primary DB

# IMPORTANT
This information is based on my own research based on open-source details I can
find (read: Google) and my intuition.

Details labelled here may be completely wrong.

# Tables
Contains the following tables:
- db_info
- packages
- obsoletes
- conflicts
- enhances
- files
- provides
- recommends
- requires
- suggests
- supplements

## db_info
Contains the following columns:

| Column Name | Description |
| - | - |
| db_version | Database version|
| checksum | The checksum of the SQLite file itself|

## packages
Contains the following columns:
| Column Name | Description |
| - | - |
| pkgKey | The primary key that represents the package |
| pkgId | ID of the package. Also the hash  for the package with hash format defined in `checksum_type` column |
| name | Name of the package |
| arch | Architecture that this package supports |
| version | Package version |
| epoch | Refer to [this description](https://rpm-packaging-guide.github.io/#epoch). TL;DR: higher epoches has higher version regardless of the actual version. This is used for packages that has version renames but is of newer version|
| release | Release version |
| summary | A short summary of the package |
| description | A description of the package |
| url | URL to the upstream project |
| time_file | Time that the package is included (?) in the repository in Unix timestamp |
| time_build | The time that the package is built in Unix timestamp |
| rpm_license | Package license |
| rpm_vendor | The vendor that provides this package |
| rpm_group | The group that this package is part of |
| rpm_buildhost | The hostname that builds this package |
| rpm_sourcerpm | The source RPM that this package is built from |
| rpm_header_start | No idea. |
| rpm_header_end | No idea. |
| size_package | Package size |
| size_installed | Size that will be occupied when the package is installed. |
| location_href | Location of the package relative to the `repodata` parent directory. |
| location_base | No idea. |
| checksum_type | The hash type of the hash inside `pkgId` column |

## obsoletes
Contains the following columns:
| Column Name | Description |
| - | - |
| name | Name of the package |
| flags | What kind of comparison it should do on resolving the version |
| epoch | Epoch that this package will obsoleted by this package |
| version | The version that this package will obsoleted by this package |
| release | The release that this package will obsoleted by this package |
| pkgKey | The package key that represents the package |

### Extra notes
Note: `flags` are defined as follows: 
- LT (obsoletes older package versions excluding the defined version)
- LE (obsolutes older package versions including the defined version)
- EQ (obsoletes the exact version defined)

## conflicts
