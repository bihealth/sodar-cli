"""Implementation of ``sodar-cli samplesheet fileexist``."""

import argparse
import sys
import uuid

from logzero import logger

# from sodar_cli import api
from sodar_cli.samplesheet.config import SampleDataFileExistsConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="project_cmd", default=run, help=argparse.SUPPRESS)
    parser.add_argument("md5_sum", help="checksum to search for", type=uuid.UUID)


def run(config, toml_config, args, _parser, _subparser, file=sys.stdout):
    """Run samplesheet fileexist command."""
    config = SampleDataFileExistsConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Looking for file's existence")
