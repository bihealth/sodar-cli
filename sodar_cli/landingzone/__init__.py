"""Implementation of sodar-cli landingzone subcommand."""

import argparse

from sodar_cli.common import run_nocmd
from sodar_cli.landingzone.config import LandingZoneConfig
from sodar_cli.landingzone.list import setup_argparse as setup_argparse_list
from sodar_cli.landingzone.retrieve import setup_argparse as setup_argparse_retrieve
from sodar_cli.landingzone.create import setup_argparse as setup_argparse_create
from sodar_cli.landingzone.validate import setup_argparse as setup_argparse_validate
from sodar_cli.landingzone.move import setup_argparse as setup_argparse_move


def setup_argparse(parser: argparse.ArgumentParser) -> None:
    """Main entry point for subcommand."""
    subparsers = parser.add_subparsers(dest="landingzone_cmd")

    setup_argparse_list(subparsers.add_parser("list", help="List landing zones."))
    setup_argparse_retrieve(subparsers.add_parser("retrieve", help="Retrieve landing zone."))
    setup_argparse_create(subparsers.add_parser("create", help="Create landing zone."))
    setup_argparse_validate(
        subparsers.add_parser("validate", help="Validate landing zone (async).")
    )
    setup_argparse_move(subparsers.add_parser("move", help="Move landing zone (async)."))


def run(config, toml_config, args, parser, subparser):
    """Main entry point for landing zone command."""
    if not args.landingzone_cmd:  # pragma: nocover
        return run_nocmd(config, args, parser, subparser)
    else:
        config = LandingZoneConfig.create(args, config, toml_config)
        return args.landingzone_cmd(config, toml_config, args, parser, subparser)
