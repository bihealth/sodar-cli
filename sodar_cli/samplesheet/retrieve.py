"""Implementation of ``sodar-cli samplesheet retrieve``."""

import argparse
import json
import sys
import uuid

import cattr
from logzero import logger

from sodar_cli import api
from sodar_cli.samplesheet.config import SampleSheetRetrieveConfig


def setup_argparse(parser):
    parser.add_argument("--hidden-cmd", dest="samplesheet_cmd", default=run, help=argparse.SUPPRESS)
    parser.add_argument(
        "project_uuid", help="UUID of project to retrieve sample sheet for", type=uuid.UUID
    )


def run(config, toml_config, args, _parser, _subparser, file=None):
    """Run samplesheet retrieve command."""
    config = SampleSheetRetrieveConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Retrieve sample sheet for project")
    result = api.samplesheet.retrieve(
        sodar_url=config.samplesheet_config.global_config.sodar_server_url,
        sodar_api_token=config.samplesheet_config.global_config.sodar_api_token,
        project_uuid=config.project_uuid,
    )
    print(json.dumps(cattr.unstructure(result)), file=(file or sys.stdout))
