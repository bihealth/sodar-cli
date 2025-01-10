"""Implementation of ``sodar-cli samplesheet download``."""

import argparse
import json
import os
import sys
import uuid

from logzero import logger

from sodar_cli import api
from sodar_cli.samplesheet.config import SampleSheetExportConfig


def setup_argparse(parser):
    parser.add_argument(
        "--hidden-cmd",
        dest="samplesheet_cmd",
        default=run,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--print-output",
        dest="print_output",
        action="store_true",
        help="Print output to stdout",
    )
    parser.add_argument("--write-output", default=None, help="Write output to given path")
    parser.add_argument(
        "--overwrite",
        default=False,
        action="store_true",
        help="Overwrite existing files",
    )
    parser.add_argument(
        "project_uuid",
        help="UUID of project to retrieve the sample sheet for",
        type=uuid.UUID,
    )


def run(config, toml_config, args, _parser, _subparser, file=None):
    """Run samplesheet download command."""
    config = SampleSheetExportConfig.create(args, config, toml_config)
    logger.info("Configuration: %s", config)
    logger.info("Exporting sample sheet to file")
    result = api.samplesheet.export(
        sodar_url=config.samplesheet_config.global_config.sodar_server_url,
        sodar_api_token=config.samplesheet_config.global_config.sodar_api_token,
        project_uuid=config.project_uuid,
    )
    if args.print_output:
        print(json.dumps(result), file=(file or sys.stdout))
    if args.write_output:
        os.makedirs(args.write_output, exist_ok=True)
        path_i = os.path.join(args.write_output, result["investigation"]["path"])
        logger.info("Writing investigation to %s", path_i)
        if os.path.exists(path_i) and not args.overwrite:  # pragma: nocover
            logger.warn("File exists and --write-output missing, skipping!")
        else:
            with open(path_i, "wt") as outputf:
                print(result["investigation"]["tsv"], file=outputf)
        for fname, study in result["studies"].items():
            path_s = os.path.join(args.write_output, fname)
            logger.info("Writing study to %s", path_s)
            if os.path.exists(path_s) and not args.overwrite:  # pragma: nocover
                logger.warn("File exists and --write-output missing, skipping!")
            else:
                with open(path_s, "wt") as outputf:
                    print(study["tsv"], file=outputf)
        for fname, assay in result["assays"].items():
            path_a = os.path.join(args.write_output, fname)
            logger.info("Writing assay to %s", path_a)
            if os.path.exists(path_a) and not args.overwrite:  # pragma: nocover
                logger.warn("File exists and --write-output missing, skipping!")
            else:
                with open(path_a, "wt") as outputf:
                    print(assay["tsv"], file=outputf)
    if not args.print_output and not args.write_output:
        logger.warn("Did nothing with result. You probably want either --write-output or --print-output")
