import typing

import cattr
from logzero import logger
import requests

from sodar_cli.api import models


def list_(*, sodar_url, sodar_api_token):
    """List projects."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]
    url_tpl = "%(sodar_url)s/project/api/list"
    url = url_tpl % {"sodar_url": sodar_url}

    logger.debug("HTTP GET request to %s", url)
    headers = {"Authorization": "Token %s" % sodar_api_token}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return cattr.structure(r.json(), typing.List[models.Project])


def retrieve(*, sodar_url, sodar_api_token, project_uuid):
    """Retrieve project information."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]
    url_tpl = "%(sodar_url)s/project/api/retrieve/%(project_uuid)s"
    url = url_tpl % {"sodar_url": sodar_url, "project_uuid": project_uuid}

    logger.debug("HTTP GET request to %s", url)
    headers = {"Authorization": "Token %s" % sodar_api_token}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return cattr.structure(r.json(), models.Project)


def create(*, sodar_url, sodar_api_token, project):
    """Retrieve project information."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]
    url_tpl = "%(sodar_url)s/project/api/create"
    url = url_tpl % {"sodar_url": sodar_url}

    logger.debug("HTTP POST request to %s", url)
    headers = {"Authorization": "Token %s" % sodar_api_token}
    data = cattr.unstructure(project)
    data.pop("sodar_uuid")
    r = requests.post(url, headers=headers, data=data)
    r.raise_for_status()
    return cattr.structure(r.json(), models.Project)


def update(*, sodar_url, sodar_api_token, project_uuid, project):
    """Update project information."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]
    url_tpl = "%(sodar_url)s/project/api/update/%(project_uuid)s"
    url = url_tpl % {"sodar_url": sodar_url, "project_uuid": project_uuid}

    logger.debug("HTTP POST request to %s", url)
    headers = {"Authorization": "Token %s" % sodar_api_token}
    data = cattr.unstructure(project)
    data.pop("sodar_uuid")
    r = requests.post(url, headers=headers, data=data)
    r.raise_for_status()
    return cattr.structure(r.json(), models.Project)
