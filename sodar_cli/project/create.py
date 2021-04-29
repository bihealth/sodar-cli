"""Implementation of ``varfish-cli project create``."""

import argparse
import sys

from logzero import logger

# from sodar_cli import api
from sodar_cli.project.config import ProjectCreateConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="project_cmd", default=run, help=argparse.SUPPRESS)


def run(config, toml_config, args, _parser, _subparser, file=sys.stdout):
    """Run landingzone retrieve command."""
    config = ProjectCreateConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Creating project")
