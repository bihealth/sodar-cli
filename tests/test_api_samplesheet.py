"""Tests for ``sodar_cli.api.samplesheet``."""

import cattr
from sodar_cli.api import samplesheet

from . import factories


def test_samplesheet_retrieve(requests_mock):
    args = {
        "sodar_url": "https://sodar.example.com/",
        "project_uuid": "46f4d0d7-b446-4a04-99c4-53cbffe952a3",
        "sodar_api_token": "token",
    }
    tpl = "%(sodar_url)ssamplesheets/api/investigation/retrieve/%(project_uuid)s"
    expected = factories.InvestigationFactory()
    requests_mock.register_uri(
        "GET",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure(expected),
    )
    result = samplesheet.retrieve(**args)
    assert expected == result


def test_samplesheets_export(requests_mock):
    args = {
        "sodar_url": "https://sodar.example.com/",
        "project_uuid": "46f4d0d7-b446-4a04-99c4-53cbffe952a3",
        "sodar_api_token": "token",
    }
    tpl = "%(sodar_url)ssamplesheets/api/export/json/%(project_uuid)s"
    expected = {"sample": "sheet"}
    requests_mock.register_uri(
        "GET",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=expected,
    )
    result = samplesheet.export(**args)
    assert expected == result


def test_samplesheets_upload(requests_mock, tmpdir):
    i_path = tmpdir / "i_example.txt"
    with i_path.open("wt") as i_file:
        print("TEST", file=i_file)

    args = {
        "sodar_url": "https://sodar.example.com/",
        "project_uuid": "46f4d0d7-b446-4a04-99c4-53cbffe952a3",
        "sodar_api_token": "token",
        "file_paths": [str(i_path)],
    }
    tpl = "%(sodar_url)ssamplesheets/api/import/%(project_uuid)s"
    expected = {"detail": "that worked"}
    requests_mock.register_uri(
        "POST",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=expected,
    )
    result = samplesheet.upload(**args)
    assert expected == result
