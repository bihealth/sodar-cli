"""Tests for ``sodar_cli.api.irodsinfo``."""

from sodar_cli.api import irodsinfo


def test_irodsinfo_retrieve(requests_mock):
    args = {
        "sodar_url": "https://sodar.example.com/",
        "sodar_api_token": "token",
    }
    url = f"{args['sodar_url']}irods/api/environment"
    expected = {"irods_environment": "take this"}
    requests_mock.register_uri(
        "GET",
        url,
        headers={"Authorization": f"Token {args['sodar_api_token']}"},
        json=expected,
    )
    result = irodsinfo.retrieve(**args)
    assert result == expected
