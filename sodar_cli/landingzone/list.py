"""Implementation of ``varfish-cli landingzone list``."""

import argparse
import sys
import uuid

from logzero import logger

# from sodar_cli import api
from sodar_cli.landingzone.config import LandingZoneListConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="landingzone_cmd", default=run, help=argparse.SUPPRESS)
    parser.add_argument(
        "project_uuid", help="UUID of the project to list landing zones for.", type=uuid.UUID
    )


def run(config, toml_config, args, _parser, _subparser, file=sys.stdout):
    """Run landingzone list command."""
    config = LandingZoneListConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Listing landing zones")
