from types import SimpleNamespace

from sodar_cli.common import CommonConfig
from sodar_cli.samplesheet import config

import pytest


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
