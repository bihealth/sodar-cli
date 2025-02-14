import typing

import cattr
from logzero import logger
import requests


from sodar_cli.api import samplesheet
from sodar_cli.api import models

ACCEPT_HEADER = {"Accept": 'application/vnd.bihealth.sodar.landingzones+json; version=1.0'}

def retrieve(*, sodar_url, sodar_api_token, landingzone_uuid):
    """Return landing zones in project."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]
    url_tpl = "%(sodar_url)s/landingzones/api/retrieve/%(landingzone_uuid)s"
    url = url_tpl % {
        "sodar_url": sodar_url,
        "landingzone_uuid": landingzone_uuid,
    }

    logger.debug("HTTP GET request to %s", url)
    headers = {"Authorization": "Token %s" % sodar_api_token, **ACCEPT_HEADER}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return cattr.structure(r.json(), models.LandingZone)


def list_(*, sodar_url, sodar_api_token, project_uuid):
    """Return landing zones in project."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]
    url_tpl = "%(sodar_url)s/landingzones/api/list/%(project_uuid)s"
    url = url_tpl % {"sodar_url": sodar_url, "project_uuid": project_uuid}

    logger.debug("HTTP GET request to %s", url)
    headers = {"Authorization": "Token %s" % sodar_api_token, **ACCEPT_HEADER}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return cattr.structure(r.json(), typing.List[models.LandingZone])


def create(*, sodar_url, sodar_api_token, project_uuid, assay_uuid=None):
    """Create landing zone in project."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]

    # Retrieve sample sheet for assay if not given.
    if not assay_uuid:
        investigation = samplesheet.retrieve(
            sodar_url=sodar_url,
            sodar_api_token=sodar_api_token,
            project_uuid=project_uuid,
        )
        if len(investigation.studies) != 1:  # pragma: no cover
            logger.error("Expected one study, found %d", len(investigation.studies))
            logger.info("Try specifying an explicit --assay parameter")
            raise Exception("Invalid number of studies in investigation!")  # TODO
        study = list(investigation.studies.values())[0]
        if len(study.assays) != 1:  # pragma: no cover
            logger.error("Expected one assay, found %d", len(study.assays))
            logger.info("Try specifying an explicit --assay parameter")
            raise Exception("Invalid number of assays in investigation!")  # TODO
        assay_uuid = list(study.assays.keys())[0]

    # Create landing zone through API.
    url_tpl = "%(sodar_url)s/landingzones/api/create/%(project_uuid)s"
    url = url_tpl % {"sodar_url": sodar_url, "project_uuid": project_uuid}
    logger.debug("HTTP POST request to %s", url)
    headers = {"Authorization": "Token %s" % sodar_api_token, **ACCEPT_HEADER}
    data = {"assay": assay_uuid}
    r = requests.post(url, data=data, headers=headers)
    r.raise_for_status()
    return cattr.structure(r.json(), models.LandingZone)


def submit_move(*, sodar_url, sodar_api_token, landingzone_uuid):
    """Move landing zone with the given UUID."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]

    # Move landing zone through API.
    url_tpl = "%(sodar_url)s/landingzones/api/submit/move/%(landingzone_uuid)s"
    url = url_tpl % {
        "sodar_url": sodar_url,
        "landingzone_uuid": landingzone_uuid,
    }
    logger.debug("HTTP POST request to %s", url)
    headers = {"Authorization": "Token %s" % sodar_api_token, **ACCEPT_HEADER}
    r = requests.post(url, headers=headers)
    r.raise_for_status()
    return retrieve(
        sodar_url=sodar_url,
        sodar_api_token=sodar_api_token,
        landingzone_uuid=r.json()["sodar_uuid"],
    )


def submit_validate(*, sodar_url, sodar_api_token, landingzone_uuid):
    """Validate landing zone with the given UUID."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]

    # Move landing zone through API.
    url_tpl = "%(sodar_url)s/landingzones/api/submit/validate/%(landingzone_uuid)s"
    url = url_tpl % {
        "sodar_url": sodar_url,
        "landingzone_uuid": landingzone_uuid,
    }
    logger.debug("HTTP POST request to %s", url)
    headers = {"Authorization": "Token %s" % sodar_api_token, **ACCEPT_HEADER}
    r = requests.post(url, headers=headers)
    r.raise_for_status()
    return retrieve(
        sodar_url=sodar_url,
        sodar_api_token=sodar_api_token,
        landingzone_uuid=r.json()["sodar_uuid"],
    )
