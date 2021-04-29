"""Implementation of sodar-cli samplesheet subcommand."""

import argparse

from sodar_cli.common import run_nocmd
from sodar_cli.samplesheet.config import SampleSheetConfig
from sodar_cli.samplesheet.retrieve import setup_argparse as setup_argparse_retrieve
from sodar_cli.samplesheet.importisa import setup_argparse as setup_argparse_import
from sodar_cli.samplesheet.export import setup_argparse as setup_argparse_export
from sodar_cli.samplesheet.fileexists import setup_argparse as setup_argparse_fileexists


def setup_argparse(parser: argparse.ArgumentParser) -> None:
    """Main entry point for subcommand."""
    subparsers = parser.add_subparsers(dest="samplesheet_cmd")

    setup_argparse_retrieve(
        subparsers.add_parser("import", help="Retrieve sample sheet for project.")
    )
    setup_argparse_import(subparsers.add_parser("import", help="Import ISA-tab into project."))
    setup_argparse_export(subparsers.add_parser("export", help="Export ISA-tab from project."))
    setup_argparse_fileexists(
        subparsers.add_parser(
            "file-exists", help="Query whether a file with the given checksum exists."
        )
    )


def run(config, toml_config, args, parser, subparser):
    """Main entry point for sample sheet command."""
    if not args.samplesheet_cmd:  # pragma: nocover
        return run_nocmd(config, args, parser, subparser)
    else:
        config = SampleSheetConfig.create(args, config, toml_config)
        return args.samplesheet_cmd(config, toml_config, args, parser, subparser)
