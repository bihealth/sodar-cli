"""Shared code."""

import attr


@attr.s(frozen=True, auto_attribs=True)
class CommonConfig:
    """Common configuration for all commands."""

    #: Verbose mode activated
    verbose: bool

    #: Whether to enable SSL verification in HTTPS requests.
    verify_ssl: bool

    #: API key to use for SODAR.
    sodar_api_token: str = attr.ib(repr=lambda value: repr(value[:4] + (len(value) - 4) * "*"))

    #: Base URL to SODAR server.
    sodar_server_url: str

    @staticmethod
    def create(args, toml_config=None):
        toml_config = toml_config or {}
        return CommonConfig(
            verbose=args.verbose,
            verify_ssl=args.verify_ssl,
            sodar_api_token=(
                args.sodar_api_token or toml_config.get("global", {}).get("sodar_api_token")
            ),
            sodar_server_url=(
                args.sodar_server_url or toml_config.get("global", {}).get("sodar_server_url")
            ),
        )


def run_nocmd(_config, _toml_config, _args, parser, subparser=None):  # pragma: no cover
    """No command given, print help and ``exit(1)``."""
    if subparser:
        subparser.print_help()
        subparser.exit(1)
    else:
        parser.print_help()
        parser.exit(1)
