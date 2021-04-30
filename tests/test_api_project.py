"""Tests for ``sodar_cli.api.project``."""

import cattr
from sodar_cli.api import project

from . import factories


def test_project_list(requests_mock):
    args = {"sodar_url": "https://sodar.example.com/", "sodar_api_token": "token"}
    tpl = "%(sodar_url)sproject/api/list"
    expected = [factories.ProjectFactory()]
    requests_mock.register_uri(
        "GET",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure(expected),
    )
    result = project.list_(**args)
    assert expected == result


def test_project_retrieve(requests_mock):
    args = {
        "sodar_url": "https://sodar.example.com/",
        "project_uuid": "46f4d0d7-b446-4a04-99c4-53cbffe952a3",
        "sodar_api_token": "token",
    }
    tpl = "%(sodar_url)sproject/api/retrieve/%(project_uuid)s"
    expected = factories.ProjectFactory()
    requests_mock.register_uri(
        "GET",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure(expected),
    )
    result = project.retrieve(**args)
    assert expected == result


def test_project_create(requests_mock):
    # Query for project
    p_args = {
        "sodar_url": "https://sodar.example.com/",
        "project_uuid": "46f4d0d7-b446-4a04-99c4-53cbffe952a3",
        "sodar_api_token": "token",
    }
    p_tpl = "%(sodar_url)sproject/api/investigation/retrieve/%(project_uuid)s"
    investigation = factories.InvestigationFactory()
    requests_mock.register_uri(
        "GET",
        p_tpl % p_args,
        headers={"Authorization": "Token %s" % p_args["sodar_api_token"]},
        json=cattr.unstructure(investigation),
    )
    # Creation of project.
    l_args = p_args.copy()
    l_args.pop("project_uuid")
    p_obj = factories.ProjectFactory()
    l_args["project"] = p_obj
    l_tpl = "%(sodar_url)sproject/api/create"
    requests_mock.register_uri(
        "POST",
        l_tpl % p_args,
        headers={"Authorization": "Token %s" % p_args["sodar_api_token"]},
        json=cattr.unstructure(p_obj),
    )
    result = project.create(**l_args)
    assert p_obj == result


def test_project_update(requests_mock):
    # Move landing zone
    m_args = {
        "sodar_url": "https://sodar.example.com/",
        "project_uuid": "46f4d0d7-b446-4a04-99c4-53cbffe952a3",
        "sodar_api_token": "token",
    }
    m_tpl = "%(sodar_url)sprojects/api/submit/move/%(project_uuid)s"
    m_result = factories.ProjectFactory(sodar_uuid=m_args["project_uuid"])
    requests_mock.register_uri(
        "POST",
        m_tpl % m_args,
        headers={"Authorization": "Token %s" % m_args["sodar_api_token"]},
        json=cattr.unstructure(m_result),
    )
    # Update project.
    r_args = m_args.copy()
    p_obj = factories.ProjectFactory()
    r_args["project"] = p_obj
    r_tpl = "%(sodar_url)sproject/api/update/%(project_uuid)s"
    requests_mock.register_uri(
        "POST",
        r_tpl % r_args,
        headers={"Authorization": "Token %s" % r_args["sodar_api_token"]},
        json=cattr.unstructure(p_obj),
    )
    result = project.update(**r_args)
    assert p_obj == result
