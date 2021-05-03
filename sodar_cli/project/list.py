"""Implementation of ``varfish-cli project list``."""

import argparse
import json
import sys

import cattr
from logzero import logger

from sodar_cli import api
from sodar_cli.project.config import ProjectListConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="project_cmd", default=run, help=argparse.SUPPRESS)


def run(config, toml_config, args, _parser, _subparser, file=None):
    """Run project list command."""
    config = ProjectListConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Listing projects")
    result = api.project.list_(
        sodar_url=config.project_config.global_config.sodar_server_url,
        sodar_api_token=config.project_config.global_config.sodar_api_token,
    )
    print(json.dumps(cattr.unstructure(result)), file=(file or sys.stdout))
