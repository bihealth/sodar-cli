"""Tests for ``sodar_cli.api.landingzone``."""

import cattr
from sodar_cli.api import landingzone

from . import factories


def test_landingzone_retrieve(requests_mock):
    args = {
        "sodar_url": "https://sodar.example.com/",
        "landing_zone_uuid": "46f4d0d7-b446-4a04-99c4-53cbffe952a3",
        "sodar_api_token": "token",
    }
    tpl = "%(sodar_url)slandingzones/api/retrieve/%(landing_zone_uuid)s"
    expected = factories.LandingZoneFactory()
    requests_mock.register_uri(
        "GET",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure(expected),
    )
    result = landingzone.retrieve(**args)
    assert expected == result


def test_landingzone_list(requests_mock):
    args = {
        "sodar_url": "https://sodar.example.com/",
        "project_uuid": "46f4d0d7-b446-4a04-99c4-53cbffe952a3",
        "sodar_api_token": "token",
    }
    tpl = "%(sodar_url)slandingzones/api/list/%(project_uuid)s"
    expected = [factories.LandingZoneFactory()]
    requests_mock.register_uri(
        "GET",
        tpl % args,
        headers={"Authorization": "Token %s" % args["sodar_api_token"]},
        json=cattr.unstructure(expected),
    )
    result = landingzone.list_(**args)
    assert expected == result


def test_landingzone_create(requests_mock):
    # Query for investigation
    i_args = {
        "sodar_url": "https://sodar.example.com/",
        "project_uuid": "46f4d0d7-b446-4a04-99c4-53cbffe952a3",
        "sodar_api_token": "token",
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
    l_args = i_args.copy()
    l_tpl = "%(sodar_url)slandingzones/api/create/%(project_uuid)s"
    landing_zone = factories.LandingZoneFactory(project=i_args["project_uuid"])
    requests_mock.register_uri(
        "POST",
        l_tpl % i_args,
        headers={"Authorization": "Token %s" % i_args["sodar_api_token"]},
        json=cattr.unstructure(landing_zone),
    )
    result = landingzone.create(**l_args)
    assert landing_zone == result


def test_landingzones_submit_move(requests_mock):
    # Move landing zone
    m_args = {
        "sodar_url": "https://sodar.example.com/",
        "landing_zone_uuid": "46f4d0d7-b446-4a04-99c4-53cbffe952a3",
        "sodar_api_token": "token",
    }
    m_tpl = "%(sodar_url)slandingzones/api/submit/move/%(landing_zone_uuid)s"
    m_result = factories.LandingZoneFactory(sodar_uuid=m_args["landing_zone_uuid"])
    requests_mock.register_uri(
        "POST",
        m_tpl % m_args,
        headers={"Authorization": "Token %s" % m_args["sodar_api_token"]},
        json=cattr.unstructure(m_result),
    )
    # Retrieve landing zone.
    r_args = m_args.copy()
    r_tpl = "%(sodar_url)slandingzones/api/retrieve/%(landing_zone_uuid)s"
    r_result = m_result
    requests_mock.register_uri(
        "GET",
        r_tpl % r_args,
        headers={"Authorization": "Token %s" % r_args["sodar_api_token"]},
        json=cattr.unstructure(r_result),
    )
    result = landingzone.submit_move(**m_args)
    assert r_result == result


def test_landingzones_submit_validate(requests_mock):
    # Move landing zone
    m_args = {
        "sodar_url": "https://sodar.example.com/",
        "landing_zone_uuid": "46f4d0d7-b446-4a04-99c4-53cbffe952a3",
        "sodar_api_token": "token",
    }
    m_tpl = "%(sodar_url)slandingzones/api/submit/validate/%(landing_zone_uuid)s"
    m_result = factories.LandingZoneFactory(sodar_uuid=m_args["landing_zone_uuid"])
    requests_mock.register_uri(
        "POST",
        m_tpl % m_args,
        headers={"Authorization": "Token %s" % m_args["sodar_api_token"]},
        json=cattr.unstructure(m_result),
    )
    # Retrieve landing zone.
    r_args = m_args.copy()
    r_tpl = "%(sodar_url)slandingzones/api/retrieve/%(landing_zone_uuid)s"
    r_result = m_result
    requests_mock.register_uri(
        "GET",
        r_tpl % r_args,
        headers={"Authorization": "Token %s" % r_args["sodar_api_token"]},
        json=cattr.unstructure(r_result),
    )
    result = landingzone.submit_validate(**m_args)
    assert r_result == result
