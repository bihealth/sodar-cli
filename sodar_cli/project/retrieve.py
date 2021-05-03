"""Implementation of ``sodar-cli project retrieve``."""

import argparse
import json
import sys
import uuid

import cattr
from logzero import logger

from sodar_cli import api
from sodar_cli.project.config import ProjectRetrieveConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="project_cmd", default=run, help=argparse.SUPPRESS)
    parser.add_argument("project_uuid", help="UUID of the project to retrieve.", type=uuid.UUID)


def run(config, toml_config, args, _parser, _subparser, file=None):
    """Run project list command."""
    config = ProjectRetrieveConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Retrieving projects")
    result = api.project.retrieve(
        sodar_url=config.project_config.global_config.sodar_server_url,
        sodar_api_token=config.project_config.global_config.sodar_api_token,
        project_uuid=config.project_uuid,
    )
    print(json.dumps(cattr.unstructure(result)), file=(file or sys.stdout))
