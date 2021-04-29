from types import SimpleNamespace

from sodar_cli.common import CommonConfig
from sodar_cli.landingzone import config

import pytest


@pytest.fixture
def args():
    return SimpleNamespace(
        verbose=False,
        verify_ssl=True,
        sodar_api_token="XXX",
        sodar_server_url="https://sodar.example.com/",
        project_uuid="123",
        landingzone_uuid="456",
        assay_uuid="789",
        config_data='{"foo": "bar"}',
        configuration="special",
        description="fancy description",
        title="some title",
    )


@pytest.fixture
def common_config(args):
    return CommonConfig.create(args)


@pytest.fixture
def landingzone_config(args, common_config):
    return config.LandingZoneConfig.create(args, common_config)


def test_landingzone_list_config(args, landingzone_config):
    config.LandingZoneListConfig.create(args, landingzone_config)


def tet_landingzone_retrieve_config(args, landingzone_config):
    config.LandingZoneRetrieveConfig.create(args, landingzone_config)


def test_landingzone_create_config(args, landingzone_config):
    config.LandingZoneCreateConfig.create(args, landingzone_config)


def test_landingzone_submit_delete_config(args, landingzone_config):
    config.LandingZoneSubmitDeleteConfig.create(args, landingzone_config)


def test_landingzone_submit_validate_config(args, landingzone_config):
    config.LandingZoneSubmitValidateConfig.create(args, landingzone_config)


def test_landingzone_submit_move_config(args, landingzone_config):
    config.LandingZoneSubmitMoveConfig.create(args, landingzone_config)
