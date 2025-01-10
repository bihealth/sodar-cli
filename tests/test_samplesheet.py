from pathlib import Path
import json
from types import SimpleNamespace

from sodar_cli.common import CommonConfig
from sodar_cli.samplesheet import config
from sodar_cli.__main__ import main
from . import factories

import cattr
import pytest


#: Common API token to use for testing.
SODAR_API_TOKEN = "XXX"
#: Common server URL to use for testing.
SODAR_SERVER_URL = "https://sodar.example.com/"


@pytest.fixture
def args():
    return SimpleNamespace(
        verbose=False,
        verify_ssl=True,
        sodar_api_token="XXX",
        sodar_server_url="https://sodar.example.com/",
        project_uuid="123",
        file_paths=[],
        md5_sum="asdf",
    )


@pytest.fixture
def common_config(args):
    return CommonConfig.create(args)


@pytest.fixture
def samplesheet_config(args, common_config):
    return config.SampleSheetConfig.create(args, common_config)


def test_samplesheet_retrieve_config(args, samplesheet_config):
    config.SampleSheetRetrieveConfig.create(args, common_config)


def test_samplesheet_import_config(args, samplesheet_config):
    config.SampleSheetImportConfig.create(args, common_config)


def test_samplesheet_export_config(args, samplesheet_config):
    config.SampleSheetExportConfig.create(args, common_config)


def test_sample_data_file_exists_config(args, samplesheet_config):
    config.SampleDataFileExistsConfig.create(args, common_config)


def test_samplesheet_retrieve(capsys, requests_mock):
    i_obj = factories.InvestigationFactory()
    args = {
        "sodar_url": SODAR_SERVER_URL,
        "sodar_api_token": SODAR_API_TOKEN,
        "project_uuid": i_obj.project,
    }
    tpl = "%(sodar_url)ssamplesheets/api/investigation/retrieve/%(project_uuid)s"
    requests_mock.register_uri(
        "GET",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure(i_obj),
    )

    main(
        [
            "--sodar-server-url",
            SODAR_SERVER_URL,
            "--sodar-api-token",
            SODAR_API_TOKEN,
            "samplesheet",
            "retrieve",
            i_obj.project,
        ]
    )
    captured = capsys.readouterr()

    assert json.dumps(cattr.unstructure(i_obj)) + "\n" == captured.out


def test_samplesheet_import(capsys, requests_mock):
    p_base = Path(__file__).parent / "data" / "isatab"
    i_obj = factories.InvestigationFactory()
    args = {
        "sodar_url": SODAR_SERVER_URL,
        "sodar_api_token": SODAR_API_TOKEN,
        "project_uuid": i_obj.project,
    }
    tpl = "%(sodar_url)ssamplesheets/api/import/%(project_uuid)s"
    requests_mock.register_uri(
        "POST",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure(i_obj),
    )

    main(
        [
            "--sodar-server-url",
            SODAR_SERVER_URL,
            "--sodar-api-token",
            SODAR_API_TOKEN,
            "samplesheet",
            "import",
            i_obj.project,
            str(p_base / "i_Investigation.txt"),
            str(p_base / "s_test.txt"),
            str(p_base / "a_test_exome_sequencing_nucleotide_sequencing.txt"),
        ]
    )
    captured = capsys.readouterr()

    assert json.dumps(cattr.unstructure(i_obj)) + "\n" == captured.out


def test_samplesheet_export(capsys, requests_mock, tmpdir):
    p_base = Path(__file__).parent / "data" / "isatab"
    result = {
        "investigation": {
            "path": "i_Investigation.txt",
            "tsv": (p_base / "i_Investigation.txt").open("rt").read(),
        },
        "studies": {"s_test.txt": {"tsv": (p_base / "s_test.txt").open("rt").read()}},
        "assays": {
            "a_test_exome_sequencing_nucleotide_sequencing.txt": {
                "tsv": (p_base / "a_test_exome_sequencing_nucleotide_sequencing.txt").open("rt").read()
            }
        },
    }

    i_obj = factories.InvestigationFactory()
    args = {
        "sodar_url": SODAR_SERVER_URL,
        "sodar_api_token": SODAR_API_TOKEN,
        "project_uuid": i_obj.project,
    }
    tpl = "%(sodar_url)ssamplesheets/api/export/json/%(project_uuid)s"
    requests_mock.register_uri(
        "GET",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=result,
    )

    main(
        [
            "--sodar-server-url",
            SODAR_SERVER_URL,
            "--sodar-api-token",
            SODAR_API_TOKEN,
            "samplesheet",
            "export",
            "--print-output",
            "--write-output",
            str(tmpdir),
            i_obj.project,
        ]
    )
    captured = capsys.readouterr()

    assert json.dumps(result) + "\n" == captured.out
    assert sorted(x.basename for x in tmpdir.listdir()) == [
        "a_test_exome_sequencing_nucleotide_sequencing.txt",
        "i_Investigation.txt",
        "s_test.txt",
    ]
