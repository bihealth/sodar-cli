"""Configuration classes for ``sodar-cli landingzone *`` commands."""

import attr
import json
import uuid

import typing

from ..common import CommonConfig


@attr.s(frozen=True, auto_attribs=True)
class LandingZoneConfig:
    """Configuration for the ``sodar-cli landingzone`` command."""

    #: Global configuration.
    global_config: CommonConfig

    @staticmethod
    def create(args, global_config, toml_config=None):
        _ = args
        # toml_config = toml_config or {}
        return LandingZoneConfig(global_config=global_config)


@attr.s(frozen=True, auto_attribs=True)
class LandingZoneListConfig:
    """Configuration for the ``sodar-cli landingzone list`` command."""

    #: Landing zone configuration.
    landingzone_config: LandingZoneConfig

    #: UUID of the project to list landing zones for.
    project_uuid: uuid.UUID

    @staticmethod
    def create(args, landingzone_config, toml_config=None):
        _ = toml_config
        # toml_config = toml_config or {}
        return LandingZoneListConfig(
            landingzone_config=landingzone_config,
            project_uuid=args.project_uuid,
        )


@attr.s(frozen=True, auto_attribs=True)
class LandingZoneRetrieveConfig:
    """Configuration for the ``sodar-cli landingzone retrieve`` command."""

    #: Landing zone configuration.
    landingzone_config: LandingZoneConfig

    #: UUID of the landing zone to retrieve.
    landingzone_uuid: uuid.UUID

    @staticmethod
    def create(args, landingzone_config, toml_config=None):
        # toml_config = toml_config or {}
        return LandingZoneRetrieveConfig(
            landingzone_config=landingzone_config,
            landingzone_uuid=args.landingzone_uuid,
        )


@attr.s(frozen=True, auto_attribs=True)
class LandingZoneCreateConfig:
    """Configuration for the ``sodar-cli landingzone create`` command."""

    #: Landing zone configuration.
    landingzone_config: LandingZoneConfig

    #: UUID of the project to create landing zone within.
    project_uuid: uuid.UUID

    #: Assay UUID
    assay_uuid: str

    #: Configuration data (JSON).
    config_data: typing.Optional[typing.Any] = None

    #: Special configuration.
    configuration: typing.Optional[str] = None

    #: Description of landing zone.
    description: typing.Optional[str] = None

    #: Suffix for the zone title.
    title: typing.Optional[str] = None

    @staticmethod
    def create(args, landingzone_config, toml_config=None):
        # toml_config = toml_config or {}
        return LandingZoneCreateConfig(
            landingzone_config=landingzone_config,
            project_uuid=args.project_uuid,
            assay_uuid=args.assay_uuid,
            config_data=json.loads(args.config_data),
            configuration=args.configuration,
            description=args.description,
            title=args.title,
        )


@attr.s(frozen=True, auto_attribs=True)
class LandingZoneSubmitDeleteConfig:
    """Configuration for the ``sodar-cli landingzone submit-delete`` command."""

    #: Landing zone configuration.
    landingzone_config: LandingZoneConfig

    #: UUID of the landing zone to submit for deletion.
    landingzone_uuid: uuid.UUID

    @staticmethod
    def create(args, landingzone_config, toml_config=None):
        # toml_config = toml_config or {}
        return LandingZoneSubmitDeleteConfig(
            landingzone_config=landingzone_config,
            landingzone_uuid=args.landingzone_uuid,
        )


@attr.s(frozen=True, auto_attribs=True)
class LandingZoneSubmitValidateConfig:
    """Configuration for the ``sodar-cli landingzone submit-validate`` command."""

    #: Landing zone configuration.
    landingzone_config: LandingZoneConfig

    #: UUID of the landing zone to submit for validation.
    landingzone_uuid: uuid.UUID

    @staticmethod
    def create(args, landingzone_config, toml_config=None):
        # toml_config = toml_config or {}
        return LandingZoneSubmitValidateConfig(
            landingzone_config=landingzone_config,
            landingzone_uuid=args.landingzone_uuid,
        )


@attr.s(frozen=True, auto_attribs=True)
class LandingZoneSubmitMoveConfig:
    """Configuration for the ``sodar-cli landingzone submit-move`` command."""

    #: Landing zone configuration.
    landingzone_config: LandingZoneConfig

    #: UUID of the landing zone to submit for moving.
    landingzone_uuid: uuid.UUID

    @staticmethod
    def create(args, landingzone_config, toml_config=None):
        # toml_config = toml_config or {}
        return LandingZoneSubmitMoveConfig(
            landingzone_config=landingzone_config,
            landingzone_uuid=args.landingzone_uuid,
        )
