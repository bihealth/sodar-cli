"""Configuration classes for ``sodar-cli samplesheet *`` commands."""

import attr
import uuid

import typing

from sodar_cli.common import CommonConfig


@attr.s(frozen=True, auto_attribs=True)
class SampleSheetConfig:
    """Configuration for the ``varfish-cli samplesheet`` command."""

    #: Global configuration.
    global_config: CommonConfig

    @staticmethod
    def create(args, global_config, toml_config=None):
        # toml_config = toml_config or {}
        return SampleSheetConfig(global_config=global_config)


@attr.s(frozen=True, auto_attribs=True)
class SampleSheetRetrieveConfig:
    """Configuration for the ``varfish-cli samplesheet retrieve`` command."""

    #: Landing zone configuration.
    samplesheet_config: SampleSheetConfig

    #: UUID of the project to retrieve sample sheet for.
    project_uuid: uuid.UUID

    @staticmethod
    def create(args, samplesheet_config, toml_config=None):
        _ = toml_config
        # toml_config = toml_config or {}
        return SampleSheetRetrieveConfig(
            samplesheet_config=samplesheet_config, project_uuid=args.project_uuid
        )


@attr.s(frozen=True, auto_attribs=True)
class SampleSheetImportConfig:
    """Configuration for the ``varfish-cli samplesheet import`` command."""

    #: Landing zone configuration.
    samplesheet_config: SampleSheetConfig

    #: UUID of the project to irods collections for.
    project_uuid: uuid.UUID

    #: Path to file(s) to upload.
    file_paths: typing.List[str]

    @staticmethod
    def create(args, samplesheet_config, toml_config=None):
        # toml_config = toml_config or {}
        return SampleSheetImportConfig(
            samplesheet_config=samplesheet_config,
            project_uuid=args.project_uuid,
            file_paths=list(args.file_paths),
        )


@attr.s(frozen=True, auto_attribs=True)
class SampleSheetExportConfig:
    """Configuration for the ``varfish-cli samplesheet export`` command."""

    #: Landing zone configuration.
    samplesheet_config: SampleSheetConfig

    #: UUID of the project to create landing zone in.
    project_uuid: uuid.UUID

    @staticmethod
    def create(args, samplesheet_config, toml_config=None):
        # toml_config = toml_config or {}
        return SampleSheetExportConfig(
            samplesheet_config=samplesheet_config, project_uuid=args.project_uuid
        )


@attr.s(frozen=True, auto_attribs=True)
class SampleDataFileExistsConfig:
    """Configuration for the ``varfish-cli samplesheet file-exists`` command."""

    #: Landing zone configuration.
    samplesheet_config: SampleSheetConfig

    #: MD5 sum to query for.
    md5_sum: str

    @staticmethod
    def create(args, samplesheet_config, toml_config=None):
        # toml_config = toml_config or {}
        return SampleDataFileExistsConfig(
            samplesheet_config=samplesheet_config, md5_sum=args.md5_sum
        )
