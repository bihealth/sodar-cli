"""Configuration classes for ``sodar-cli project *`` commands."""

import attr
import uuid

import typing

from ..common import CommonConfig


@attr.s(frozen=True, auto_attribs=True)
class ProjectConfig:
    """Configuration for the ``sodar-cli project`` command."""

    #: Global configuration.
    global_config: CommonConfig

    @staticmethod
    def create(args, global_config, toml_config=None):
        # toml_config = toml_config or {}
        return ProjectConfig(global_config=global_config)


@attr.s(frozen=True, auto_attribs=True)
class ProjectListConfig:
    """Configuration for the ``sodar-cli project list`` command."""

    #: Landing zone configuration.
    project_config: ProjectConfig

    @staticmethod
    def create(args, project_config, toml_config=None):
        _ = toml_config
        _ = args
        # toml_config = toml_config or {}
        return ProjectListConfig(project_config=project_config)


@attr.s(frozen=True, auto_attribs=True)
class ProjectRetrieveConfig:
    """Configuration for the ``sodar-cli project retrieve`` command."""

    #: Landing zone configuration.
    project_config: ProjectConfig

    #: UUID of the project to retrieve landing zones for.
    project_uuid: uuid.UUID

    @staticmethod
    def create(args, project_config, toml_config=None):
        _ = toml_config
        # toml_config = toml_config or {}
        return ProjectRetrieveConfig(project_config=project_config, project_uuid=args.project_uuid)


@attr.s(frozen=True, auto_attribs=True)
class ProjectCreateConfig:
    """Configuration for the ``sodar-cli project create`` command."""

    #: Landing zone configuration.
    project_config: ProjectConfig

    #: Project title.
    title: str
    #: Project type, one of ``"PROJECT"`` or ``"CATEGORY"``
    type: str
    #: Parent category UUID.
    parent: typing.Optional[str] = None
    #: Project description.
    description: typing.Optional[str] = None
    #: Project README, supports markdown.
    readme: typing.Optional[str] = None

    @staticmethod
    def create(args, project_config, toml_config=None):
        # toml_config = toml_config or {}
        return ProjectCreateConfig(
            project_config=project_config,
            title=args.title,
            type=args.type,
            parent=args.parent_uuid,
            description=args.description,
            readme=args.readme,
        )


@attr.s(frozen=True, auto_attribs=True)
class ProjectUpdateConfig:
    """Configuration for the ``sodar-cli project update`` command."""

    #: Landing zone configuration.
    project_config: ProjectConfig

    #: UUID of the project to update.
    project_uuid: uuid.UUID

    #: Project title.
    title: str
    #: Project type, one of ``"PROJECT"`` or ``"CATEGORY"``
    type: str
    #: Parent category UUID.
    parent: str
    #: Project description.
    description: typing.Optional[str] = None
    #: Project README, supports markdown.
    readme: typing.Optional[str] = None

    @staticmethod
    def create(args, project_config, toml_config=None):
        # toml_config = toml_config or {}
        return ProjectUpdateConfig(
            project_config=project_config,
            project_uuid=args.project_uuid,
            title=args.title,
            type=args.type,
            parent=args.parent_uuid,
            description=args.description,
            readme=args.readme,
        )
