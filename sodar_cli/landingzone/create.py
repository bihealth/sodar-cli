"""Implementation of ``sodar-cli landingzone create``."""

import argparse
import sys
import json
import uuid

import cattr
from logzero import logger

from sodar_cli import api
from sodar_cli.landingzone.config import LandingZoneListConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="landingzone_cmd", default=run, help=argparse.SUPPRESS)
    parser.add_argument(
        "project_uuid", help="UUID of the project to create landing zone within.", type=uuid.UUID
    )


def run(config, toml_config, args, _parser, _subparser, file=None):
    """Run landingzone create command."""
    config = LandingZoneListConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Creating landing zone")
    result = api.landingzone.create(
        sodar_url=config.landingzone_config.global_config.sodar_server_url,
        sodar_api_token=config.landingzone_config.global_config.sodar_api_token,
        project_uuid=config.project_uuid,
    )
    print(json.dumps(cattr.unstructure(result)), file=(file or sys.stdout))
