import json
from types import SimpleNamespace

import cattr
import pytest

from sodar_cli.common import CommonConfig
from sodar_cli.landingzone import config
from sodar_cli.__main__ import main
from . import factories


#: Common API token to use for testing.
SODAR_API_TOKEN = "XXX"
#: Common server URL to use for testing.
SODAR_SERVER_URL = "https://sodar.example.com/"


@pytest.fixture
def args():
    return SimpleNamespace(
        verbose=False,
        verify_ssl=True,
        sodar_api_token=SODAR_API_TOKEN,
        sodar_server_url=SODAR_SERVER_URL,
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


def test_landingzone_retrieve_config(args, landingzone_config):
    config.LandingZoneRetrieveConfig.create(args, landingzone_config)


def test_landingzone_create_config(args, landingzone_config):
    config.LandingZoneCreateConfig.create(args, landingzone_config)


def test_landingzone_submit_delete_config(args, landingzone_config):
    config.LandingZoneSubmitDeleteConfig.create(args, landingzone_config)


def test_landingzone_submit_validate_config(args, landingzone_config):
    config.LandingZoneSubmitValidateConfig.create(args, landingzone_config)


def test_landingzone_submit_move_config(args, landingzone_config):
    config.LandingZoneSubmitMoveConfig.create(args, landingzone_config)


def test_call_landingzone_list(capsys, requests_mock):
    project = factories.ProjectFactory()
    lz_obj = factories.LandingZoneFactory(project=project.sodar_uuid)
    args = {
        "sodar_url": SODAR_SERVER_URL,
        "sodar_api_token": SODAR_API_TOKEN,
        "project_uuid": project.sodar_uuid,
    }
    tpl = "%(sodar_url)slandingzones/api/list/%(project_uuid)s"
    requests_mock.register_uri(
        "GET",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure([lz_obj]),
    )

    main(
        [
            "--sodar-server-url",
            SODAR_SERVER_URL,
            "--sodar-api-token",
            SODAR_API_TOKEN,
            "landingzone",
            "list",
            project.sodar_uuid,
        ]
    )
    captured = capsys.readouterr()

    assert json.dumps(cattr.unstructure([lz_obj])) + "\n" == captured.out


def test_call_landingzone_retrieve(capsys, requests_mock):
    lz_obj = factories.LandingZoneFactory()
    args = {
        "sodar_url": SODAR_SERVER_URL,
        "sodar_api_token": SODAR_API_TOKEN,
        "landingzone_uuid": lz_obj.sodar_uuid,
    }
    tpl = "%(sodar_url)slandingzones/api/retrieve/%(landingzone_uuid)s"
    requests_mock.register_uri(
        "GET",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure(lz_obj),
    )

    main(
        [
            "--sodar-server-url",
            SODAR_SERVER_URL,
            "--sodar-api-token",
            SODAR_API_TOKEN,
            "landingzone",
            "retrieve",
            lz_obj.sodar_uuid,
        ]
    )
    captured = capsys.readouterr()

    assert json.dumps(cattr.unstructure(lz_obj)) + "\n" == captured.out


def test_call_landingzone_create(capsys, requests_mock):
    # Query project information.
    project = factories.ProjectFactory()
    i_args = {
        "sodar_url": SODAR_SERVER_URL,
        "sodar_api_token": SODAR_API_TOKEN,
        "project_uuid": project.sodar_uuid,
    }
    i_tpl = "%(sodar_url)ssamplesheets/api/investigation/retrieve/%(project_uuid)s"
    investigation = factories.InvestigationFactory()
    requests_mock.register_uri(
        "GET",
        i_tpl % i_args,
        headers={"Authorization": "Token %s" % i_args["sodar_api_token"]},
        json=cattr.unstructure(investigation),
    )
    # Creation of landing zone.
    l_tpl = "%(sodar_url)slandingzones/api/create/%(project_uuid)s"
    lz_obj = factories.LandingZoneFactory(project=i_args["project_uuid"])
    requests_mock.register_uri(
        "POST",
        l_tpl % i_args,
        headers={"Authorization": "Token %s" % i_args["sodar_api_token"]},
        json=cattr.unstructure(lz_obj),
    )

    main(
        [
            "--sodar-server-url",
            SODAR_SERVER_URL,
            "--sodar-api-token",
            SODAR_API_TOKEN,
            "landingzone",
            "create",
            project.sodar_uuid,
        ]
    )
    captured = capsys.readouterr()

    assert json.dumps(cattr.unstructure(lz_obj)) + "\n" == captured.out


def test_call_landingzone_submit_move(capsys, requests_mock):
    lz_obj = factories.LandingZoneFactory()
    # Move landing zone
    m_args = {
        "sodar_url": SODAR_SERVER_URL,
        "sodar_api_token": SODAR_API_TOKEN,
        "landingzone_uuid": lz_obj.sodar_uuid,
    }
    m_tpl = "%(sodar_url)slandingzones/api/submit/move/%(landingzone_uuid)s"
    m_result = factories.LandingZoneFactory(sodar_uuid=m_args["landingzone_uuid"])
    requests_mock.register_uri(
        "POST",
        m_tpl % m_args,
        headers={"Authorization": "Token %s" % m_args["sodar_api_token"]},
        json=cattr.unstructure(m_result),
    )
    # Retrieve landing zone.
    r_args = m_args.copy()
    r_tpl = "%(sodar_url)slandingzones/api/retrieve/%(landingzone_uuid)s"
    r_result = m_result
    requests_mock.register_uri(
        "GET",
        r_tpl % r_args,
        headers={"Authorization": "Token %s" % r_args["sodar_api_token"]},
        json=cattr.unstructure(r_result),
    )

    main(
        [
            "--sodar-server-url",
            SODAR_SERVER_URL,
            "--sodar-api-token",
            SODAR_API_TOKEN,
            "landingzone",
            "move",
            lz_obj.sodar_uuid,
        ]
    )
    captured = capsys.readouterr()

    assert json.dumps(cattr.unstructure(r_result)) + "\n" == captured.out


def test_call_landingzone_submit_validate(capsys, requests_mock):
    lz_obj = factories.LandingZoneFactory()
    # Move landing zone
    m_args = {
        "sodar_url": SODAR_SERVER_URL,
        "sodar_api_token": SODAR_API_TOKEN,
        "landingzone_uuid": lz_obj.sodar_uuid,
    }
    m_tpl = "%(sodar_url)slandingzones/api/submit/validate/%(landingzone_uuid)s"
    m_result = factories.LandingZoneFactory(sodar_uuid=m_args["landingzone_uuid"])
    requests_mock.register_uri(
        "POST",
        m_tpl % m_args,
        headers={"Authorization": "Token %s" % m_args["sodar_api_token"]},
        json=cattr.unstructure(m_result),
    )
    # Retrieve landing zone.
    r_args = m_args.copy()
    r_tpl = "%(sodar_url)slandingzones/api/retrieve/%(landingzone_uuid)s"
    r_result = m_result
    requests_mock.register_uri(
        "GET",
        r_tpl % r_args,
        headers={"Authorization": "Token %s" % r_args["sodar_api_token"]},
        json=cattr.unstructure(r_result),
    )

    main(
        [
            "--sodar-server-url",
            SODAR_SERVER_URL,
            "--sodar-api-token",
            SODAR_API_TOKEN,
            "landingzone",
            "validate",
            lz_obj.sodar_uuid,
        ]
    )
    captured = capsys.readouterr()

    assert json.dumps(cattr.unstructure(r_result)) + "\n" == captured.out
