from types import SimpleNamespace

from sodar_cli.common import CommonConfig
from sodar_cli.project import config

import pytest


@pytest.fixture
def args():
    return SimpleNamespace(
        verbose=False,
        verify_ssl=True,
        sodar_api_token="XXX",
        sodar_server_url="https://sodar.example.com/",
        project_uuid="123",
        title="fancy title",
        type="PROJECT",
        owner_uuid="456",
        parent_uuid="789",
        description="fancy description",
        readme="**very** fancy readme",
    )


@pytest.fixture
def common_config(args):
    return CommonConfig.create(args)


@pytest.fixture
def project_config(args, common_config):
    return config.ProjectConfig.create(args, common_config)


def test_project_list_config(args, project_config):
    config.ProjectListConfig.create(args, project_config)


def test_project_retrieve_config(args, project_config):
    config.ProjectRetrieveConfig.create(args, project_config)


def test_project_create_config(args, project_config):
    config.ProjectCreateConfig.create(args, project_config)


def test_project_update_config(args, project_config):
    config.ProjectUpdateConfig.create(args, project_config)
