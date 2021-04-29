"""Implementation of sodar-cli project subcommand."""

import argparse

from sodar_cli.common import run_nocmd
from sodar_cli.project.config import ProjectConfig
from sodar_cli.project.list import setup_argparse as setup_argparse_list
from sodar_cli.project.retrieve import setup_argparse as setup_argparse_retrieve
from sodar_cli.project.create import setup_argparse as setup_argparse_create
from sodar_cli.project.update import setup_argparse as setup_argparse_update


def setup_argparse(parser: argparse.ArgumentParser) -> None:
    """Main entry point for subcommand."""
    subparsers = parser.add_subparsers(dest="project_cmd")

    setup_argparse_list(subparsers.add_parser("list", help="List Projects."))
    setup_argparse_retrieve(subparsers.add_parser("retrieve", help="Retrieve project."))
    setup_argparse_create(
        subparsers.add_parser("create", help="Create project (there is no delete!).")
    )
    setup_argparse_update(subparsers.add_parser("delete", help="Update project."))


def run(config, toml_config, args, parser, subparser):
    """Main entry point for case command."""
    if not args.case_cmd:  # pragma: nocover
        return run_nocmd(config, args, parser, subparser)
    else:
        config = ProjectConfig.create(args, config, toml_config)
        return args.project_cmd(config, toml_config, args, parser, subparser)
