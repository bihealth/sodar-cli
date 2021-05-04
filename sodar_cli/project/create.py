"""Implementation of ``sodar-cli project create``."""

import argparse
import json
import sys

import cattr
from logzero import logger

from sodar_cli import api
from sodar_cli.project.config import ProjectCreateConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="project_cmd", default=run, help=argparse.SUPPRESS)
    parser.add_argument("--title", required=True, help="Title of the project")
    parser.add_argument("--parent-uuid", required=True, help="UUID of the parent project")
    parser.add_argument("--owner-uuid", required=True, help="UUID of the owner")
    parser.add_argument("--type", default="PROJECT", help="Type of the project [PROJECT, CATEGORY]")
    parser.add_argument("--description", help="Description text, optional")
    parser.add_argument("--readme", help="README text, markdown allowed, optional")


def run(config, toml_config, args, _parser, _subparser, file=None):
    """Run landingzone retrieve command."""
    config = ProjectCreateConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Creating project")
    project = api.Project(
        sodar_uuid=None,
        title=args.title,
        type=args.type,
        parent=args.parent_uuid,
        description=args.description,
        readme=args.readme,
    )
    result = api.project.create(
        sodar_url=config.project_config.global_config.sodar_server_url,
        sodar_api_token=config.project_config.global_config.sodar_api_token,
        project=project,
    )
    print(json.dumps(cattr.unstructure(result)), file=(file or sys.stdout))
