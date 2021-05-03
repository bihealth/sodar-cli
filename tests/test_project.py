from types import SimpleNamespace

import cattr
import json

from sodar_cli.common import CommonConfig
from sodar_cli.project import config
from sodar_cli.__main__ import main
from . import factories

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
        title="fancy title",
        type="PROJECT",
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


def test_project_retrieve(capsys, requests_mock):
    p_obj = factories.ProjectFactory()
    args = {
        "sodar_url": SODAR_SERVER_URL,
        "sodar_api_token": SODAR_API_TOKEN,
        "project_uuid": p_obj.sodar_uuid,
    }
    tpl = "%(sodar_url)sproject/api/retrieve/%(project_uuid)s"
    requests_mock.register_uri(
        "GET",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure(p_obj),
    )

    main(
        [
            "--sodar-server-url",
            SODAR_SERVER_URL,
            "--sodar-api-token",
            SODAR_API_TOKEN,
            "project",
            "retrieve",
            p_obj.sodar_uuid,
        ]
    )
    captured = capsys.readouterr()

    assert json.dumps(cattr.unstructure(p_obj)) + "\n" == captured.out


def test_project_list(capsys, requests_mock):
    args = {"sodar_url": SODAR_SERVER_URL, "sodar_api_token": SODAR_API_TOKEN}
    tpl = "%(sodar_url)sproject/api/list"
    p_obj = factories.ProjectFactory()
    requests_mock.register_uri(
        "GET",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure([p_obj]),
    )

    main(
        [
            "--sodar-server-url",
            SODAR_SERVER_URL,
            "--sodar-api-token",
            SODAR_API_TOKEN,
            "project",
            "list",
        ]
    )
    captured = capsys.readouterr()

    assert json.dumps(cattr.unstructure([p_obj])) + "\n" == captured.out


def test_project_create(capsys, requests_mock):
    p_obj = factories.ProjectFactory()
    args = {"sodar_url": SODAR_SERVER_URL, "sodar_api_token": SODAR_API_TOKEN}
    args["project"] = p_obj
    tpl = "%(sodar_url)sproject/api/create"
    requests_mock.register_uri(
        "POST",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure(p_obj),
    )

    main(
        [
            "--sodar-server-url",
            SODAR_SERVER_URL,
            "--sodar-api-token",
            SODAR_API_TOKEN,
            "project",
            "create",
        ]
    )
    captured = capsys.readouterr()

    assert json.dumps(cattr.unstructure(p_obj)) + "\n" == captured.out


def test_project_update(capsys, requests_mock):
    p_obj = factories.ProjectFactory()
    args = {
        "sodar_url": SODAR_SERVER_URL,
        "sodar_api_token": SODAR_API_TOKEN,
        "project_uuid": p_obj.sodar_uuid,
    }
    tpl = "%(sodar_url)sproject/api/update/%(project_uuid)s"
    requests_mock.register_uri(
        "POST",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure(p_obj),
    )

    main(
        [
            "--sodar-server-url",
            SODAR_SERVER_URL,
            "--sodar-api-token",
            SODAR_API_TOKEN,
            "project",
            "update",
            p_obj.sodar_uuid,
        ]
    )
    captured = capsys.readouterr()

    assert json.dumps(cattr.unstructure(p_obj)) + "\n" == captured.out
