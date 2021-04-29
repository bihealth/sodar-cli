"""Implementation of ``varfish-cli samplesheet retrieve``."""

import argparse
import sys
import uuid

from logzero import logger

# from sodar_cli import api
from sodar_cli.samplesheet.config import SampleSheetRetrieveConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="project_cmd", default=run, help=argparse.SUPPRESS)
    parser.add_argument(
        "project_uuid", help="UUID of project to retrieve sample sheet for", type=uuid.UUID
    )


def run(config, toml_config, args, _parser, _subparser, file=sys.stdout):
    """Run samplesheet import command."""
    config = SampleSheetRetrieveConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Retrieve sample sheet for project")
