"""Implementation of ``varfish-cli landingzone validate``."""

import argparse
import json
import sys
import uuid

import cattr
from logzero import logger

from sodar_cli import api
from sodar_cli.landingzone.config import LandingZoneSubmitValidateConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="landingzone_cmd", default=run, help=argparse.SUPPRESS)
    parser.add_argument(
        "landingzone_uuid", help="UUID of the landing zone to validate.", type=uuid.UUID
    )


def run(config, toml_config, args, _parser, _subparser, file=None):
    """Run landingzone retrieve command."""
    config = LandingZoneSubmitValidateConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Validating landing zone")
    result = api.landingzone.submit_validate(
        sodar_url=config.landingzone_config.global_config.sodar_server_url,
        sodar_api_token=config.landingzone_config.global_config.sodar_api_token,
        landingzone_uuid=config.landingzone_uuid,
    )
    print(json.dumps(cattr.unstructure(result)), file=(file or sys.stdout))
