"""Implementation of ``sodar-cli landingzone move``."""

import argparse
import sys
import json
import uuid

import cattr
from logzero import logger

from sodar_cli import api
from sodar_cli.landingzone.config import LandingZoneSubmitMoveConfig


def setup_argparse(parser):
    parser.add_argument(
        "--hidden-cmd",
        dest="landingzone_cmd",
        default=run,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "landingzone_uuid",
        help="UUID of the landing zone to move.",
        type=uuid.UUID,
    )


def run(config, toml_config, args, _parser, _subparser, file=None):
    """Run landingzone create command."""
    config = LandingZoneSubmitMoveConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Moving landing zone")
    result = api.landingzone.retrieve(
        sodar_url=config.landingzone_config.global_config.sodar_server_url,
        sodar_api_token=config.landingzone_config.global_config.sodar_api_token,
        landingzone_uuid=config.landingzone_uuid,
    )
    print(json.dumps(cattr.unstructure(result)), file=(file or sys.stdout))
