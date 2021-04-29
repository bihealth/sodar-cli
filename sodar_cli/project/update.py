"""Implementation of ``varfish-cli project update``."""

import argparse
import sys
import uuid

from logzero import logger

# from sodar_cli import api
from sodar_cli.project.config import ProjectUpdateConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="project_cmd", default=run, help=argparse.SUPPRESS)
    parser.add_argument("project_uuid", help="UUID of the project to update.", type=uuid.UUID)


def run(config, toml_config, args, _parser, _subparser, file=sys.stdout):
    """Run landingzone retrieve command."""
    config = ProjectUpdateConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Deleting project")
