"""Main entry point for SODAR CLI."""

import argparse
import logging
import os
import sys

import logzero
import toml
from logzero import logger

from sodar_cli import __version__
from sodar_cli.common import run_nocmd, CommonConfig
from sodar_cli.landingzone import setup_argparse as setup_argparse_landingzone
from sodar_cli.landingzone import run as run_landingzone
from sodar_cli.project import setup_argparse as setup_argparse_project
from sodar_cli.project import run as run_project
from sodar_cli.samplesheet import setup_argparse as setup_argparse_samplesheet
from sodar_cli.samplesheet import run as run_samplesheet

#: Paths to search the global configuration in.
GLOBAL_CONFIG_PATHS = ("~/.sodarrc.toml",)


def setup_argparse_only():  # pragma: nocover
    """Wrapper for ``setup_argparse()`` that only returns the parser.

    Only used in sphinx documentation via ``sphinx-argparse``.
    """
    return setup_argparse()[0]


def setup_argparse():
    """Create argument parser."""
    # Construct argument parser and set global options.
    parser = argparse.ArgumentParser(prog="sodar-cli")
    parser.add_argument("--verbose", action="store_true", default=False, help="Increase verbosity.")
    parser.add_argument("--version", action="version", version="%%(prog)s %s" % __version__)

    group = parser.add_argument_group("Basic Configuration")
    group.add_argument(
        "--no-verify-ssl",
        dest="verify_ssl",
        default=True,
        action="store_false",
        help="Disable HTTPS SSL verification",
    )
    group.add_argument(
        "--config",
        default=os.environ.get("SODAR_CONFIG_PATH", None),
        help="Path to configuration file.",
    )
    group.add_argument(
        "--sodar-server-url",
        default=os.environ.get("SODAR_SERVER_URL", None),
        help="SODAR server URL key to use, defaults to env SODAR_SERVER_URL.",
    )
    group.add_argument(
        "--sodar-api-token",
        default=os.environ.get("SODAR_API_TOKEN", None),
        help="SODAR API token to use, defaults to env SODAR_API_TOKEN.",
    )

    # Add sub parsers for each argument.
    subparsers = parser.add_subparsers(dest="cmd")

    setup_argparse_project(subparsers.add_parser("project", help="Work with projects."))
    setup_argparse_samplesheet(
        subparsers.add_parser("samplesheet", help="Work with sample sheets.")
    )
    setup_argparse_landingzone(
        subparsers.add_parser("landingzone", help="Work with landing zones.")
    )

    return parser, subparsers


def main(argv=None):
    """Main entry point before parsing command line arguments."""
    # Setup command line parser.
    parser, subparsers = setup_argparse()

    # Actually parse command line arguments.
    args = parser.parse_args(argv)

    # Setup logging incl. verbosity.
    if args.verbose:  # pragma: no cover
        level = logging.DEBUG
    else:
        # Remove module name and line number if not running in debug mode.s
        formatter = logzero.LogFormatter(
            fmt="%(color)s[%(levelname)1.1s %(asctime)s]%(end_color)s %(message)s"
        )
        logzero.formatter(formatter)
        level = logging.INFO
    logzero.loglevel(level=level)

    # Load configuration, if any.
    if args.config:
        config_paths = (args.config,)
    else:
        config_paths = GLOBAL_CONFIG_PATHS
    for config_path in config_paths:
        config_path = os.path.expanduser(os.path.expandvars(config_path))
        if os.path.exists(config_path):
            with open(config_path, "rt") as tomlf:
                toml_config = toml.load(tomlf)
            break
    else:
        toml_config = None
        logger.info("Could not find any of the global configuration files %s.", config_paths)

    # Merge configuration from command line/environment args and configuration file.
    config = CommonConfig.create(args, toml_config)

    # Handle the actual command line.
    cmds = {
        None: run_nocmd,
        "project": run_project,
        "landingzone": run_landingzone,
        "samplesheet": run_samplesheet,
    }

    res = cmds[args.cmd](
        config, toml_config, args, parser, subparsers.choices[args.cmd] if args.cmd else None
    )
    if not res:
        logger.info("All done. Have a nice day!")
    else:  # pragma: nocover
        logger.error("Something did not work out correctly.")
    return res


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv))
