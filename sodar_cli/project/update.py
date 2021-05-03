"""Implementation of ``sodar-cli project update``."""

import argparse
import sys
import json
import uuid

import cattr
from logzero import logger

from sodar_cli import api
from sodar_cli.project.config import ProjectUpdateConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="project_cmd", default=run, help=argparse.SUPPRESS)
    parser.add_argument("project_uuid", help="UUID of the project to update.", type=uuid.UUID)
    parser.add_argument("--title", default="Project Title", help="Title of the project")
    parser.add_argument(
        "--type", default="Project Type", help="Type of the project [PROJECT, CATEGORY]"
    )
    parser.add_argument("--parent-uuid", help="UUID of the parent project, if any")
    parser.add_argument("--description", help="Description text, optional")
    parser.add_argument("--readme", help="README text, markdown allowed, optional")


def run(config, toml_config, args, _parser, _subparser, file=None):
    """Run landingzone retrieve command."""
    config = ProjectUpdateConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Creating project")
    project = api.Project(
        sodar_uuid=args.project_uuid,
        title=args.title,
        type=args.type,
        parent_uuid=args.parent_uuid,
        description=args.description,
        readme=args.readme,
    )
    result = api.project.update(
        sodar_url=config.project_config.global_config.sodar_server_url,
        sodar_api_token=config.project_config.global_config.sodar_api_token,
        project_uuid=config.project_uuid,
        project=project,
    )
    print(json.dumps(cattr.unstructure(result)), file=(file or sys.stdout))
