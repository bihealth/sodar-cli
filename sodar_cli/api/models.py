"""Data models for supporting the SODAR CLI."""

import datetime
import typing
import uuid

import attr
import cattr
import dateutil.parser


def _setup_converter() -> cattr.Converter:
    result = cattr.Converter()
    result.register_structure_hook(uuid.UUID, lambda d, _: uuid.UUID(d))
    result.register_unstructure_hook(uuid.UUID, str)
    result.register_structure_hook(datetime.datetime, lambda d, _: dateutil.parser.parse(d))
    result.register_unstructure_hook(
        datetime.datetime,
        lambda obj: obj.replace(tzinfo=datetime.timezone.utc)
        .astimezone()
        .replace(microsecond=0)
        .isoformat(),
    )
    return result


#: cattr Converter to use
CONVERTER = _setup_converter()


@attr.s(frozen=True, auto_attribs=True)
class User:
    """Represents a user in the SODAR API."""

    #: UUID of the user
    sodar_uuid: str
    #: Username of the user
    username: str
    #: Real name of the user
    name: str
    #: Email address of the user
    email: str
    #: Superuser status of the user
    is_superuser: bool


@attr.s(frozen=True, auto_attribs=True)
class RoleAssignment:
    sodar_uuid: str
    role: str
    user: User


@attr.s(frozen=True, auto_attribs=True)
class Project:
    sodar_uuid: str
    title: str
    type: str
    roles: typing.Optional[typing.Dict[str, RoleAssignment]] = None
    submit_status: typing.Optional[str] = None
    parent: typing.Optional[str] = None
    parent: typing.Optional[str] = None
    readme: typing.Optional[str] = None
    description: typing.Optional[str] = None


@attr.s(frozen=True, auto_attribs=True)
class OntologyTermRef:
    name: str
    accession: typing.Optional[str] = None
    ontology_name: typing.Optional[str] = None


@attr.s(frozen=True, auto_attribs=True, kw_only=True)
class Assay:
    sodar_uuid: typing.Optional[str] = None
    file_name: str
    irods_path: str
    technology_platform: str
    technology_type: OntologyTermRef
    measurement_type: OntologyTermRef
    comments: typing.Dict[str, str]


@attr.s(frozen=True, auto_attribs=True, kw_only=True)
class Study:
    sodar_uuid: typing.Optional[str] = None
    identifier: str
    file_name: str
    irods_path: str
    title: str
    description: str
    comments: typing.Dict[str, str]
    assays: typing.Dict[str, Assay]


@attr.s(frozen=True, auto_attribs=True, kw_only=True)
class Investigation:
    sodar_uuid: typing.Optional[str] = None
    archive_name: str
    comments: typing.Any
    description: str
    file_name: str
    identifier: str
    irods_status: bool
    parser_version: str
    project: str
    studies: typing.Dict[str, Study]
    title: str


@attr.s(frozen=True, auto_attribs=True, kw_only=True)
class LandingZone:
    """Represent a landing zone in the SODAR API."""

    #: UUID of the landing zone.
    sodar_uuid: typing.Optional[str] = None
    #: Date of last modification.
    date_modified: str

    #: UUID of the containing project.
    project: str
    #: Status of the landing zone.
    status: str
    #: Status information string.
    status_info: str
    #: Is write access locked for the landing zone?
    status_locked: bool
    #: Title of the landing zone.
    title: str
    #: Description of the landing zone.
    description: str
    #: Message displayed to users on successful moving of zone
    user_message: str
    #: Owning user.
    user: User

    #: UUID of the related assay.
    assay: str
    #: Optional configuration name.
    configuration: typing.Optional[typing.Any] = None
    #: Optional configuration data.
    config_data: typing.Optional[typing.Any] = None
    #: Path in iRODS.
    irods_path: str
