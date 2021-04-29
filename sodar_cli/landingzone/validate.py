"""Implementation of ``varfish-cli landingzone validate``."""

import argparse
import sys
import uuid

from logzero import logger

# from sodar_cli import api
from sodar_cli.landingzone.config import LandingZoneSubmitValidateConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="landingzone_cmd", default=run, help=argparse.SUPPRESS)
    parser.add_argument(
        "landingzone_uuid", help="UUID of the landing zone to validate.", type=uuid.UUID
    )


def run(config, toml_config, args, _parser, _subparser, file=sys.stdout):
    """Run landingzone retrieve command."""
    config = LandingZoneSubmitValidateConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Validating landing zone")
