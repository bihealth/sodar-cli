"""Implementation of ``sodar-cli samplesheet import``."""

import argparse
import json
import sys
import uuid

import cattr
from logzero import logger

from sodar_cli import api
from sodar_cli.samplesheet.config import SampleSheetImportConfig


def setup_argparse(parser):
    parser.add_argument(
        "--hidden-cmd",
        dest="samplesheet_cmd",
        default=run,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "project_uuid",
        help="UUID of project to import ISA tab for",
        type=uuid.UUID,
    )
    parser.add_argument(
        "file_paths",
        metavar="files",
        nargs="+",
        help="paths to files to import",
    )


def run(config, toml_config, args, _parser, _subparser, file=None):
    """Run samplesheet import command."""
    config = SampleSheetImportConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Import ISA-tab sample sheets into project")
    result = api.samplesheet.upload(
        sodar_url=config.samplesheet_config.global_config.sodar_server_url,
        sodar_api_token=config.samplesheet_config.global_config.sodar_api_token,
        project_uuid=config.project_uuid,
        file_paths=config.file_paths,
    )
    print(json.dumps(cattr.unstructure(result)), file=(file or sys.stdout))
