"""Implementation of ``varfish-cli project list``."""

import argparse
import sys

from logzero import logger

# from sodar_cli import api
from sodar_cli.project.config import ProjectListConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="project_cmd", default=run, help=argparse.SUPPRESS)


def run(config, toml_config, args, _parser, _subparser, file=sys.stdout):
    """Run project list command."""
    config = ProjectListConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Listing projects")
