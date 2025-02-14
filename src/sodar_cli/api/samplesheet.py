import contextlib
import pathlib

import cattr
from logzero import logger
import requests


from sodar_cli.api import models

ACCEPT_HEADER = {"Accept": "application/vnd.bihealth.sodar.samplesheets+json; version=1.0"}

def retrieve(*, sodar_url, sodar_api_token, project_uuid):
    """Get investigation information."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]
    url_tpl = "%(sodar_url)s/samplesheets/api/investigation/retrieve/%(project_uuid)s"
    url = url_tpl % {"sodar_url": sodar_url, "project_uuid": project_uuid}

    logger.debug("HTTP GET request to %s", url)
    headers = {"Authorization": "Token %s" % sodar_api_token, **ACCEPT_HEADER}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    # # TODO: remove workaround once SODAR directly returns sodar_uuid
    # tmp = r.json()
    # for study_sodar_uuid, study in tmp["studies"].items():
    #     study["sodar_uuid"] = study_sodar_uuid
    #     for assay_sodar_uuid, assay in study["assays"].items():
    #         assay["sodar_uuid"] = assay_sodar_uuid
    return cattr.structure(r.json(), models.Investigation)


def export(*, sodar_url, sodar_api_token, project_uuid):
    """Get ISA-tab sample sheet from SODAR."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]
    url_tpl = "%(sodar_url)s/samplesheets/api/export/json/%(project_uuid)s"
    url = url_tpl % {"sodar_url": sodar_url, "project_uuid": project_uuid}

    logger.debug("HTTP GET request to %s", url)
    headers = {"Authorization": "Token %s" % sodar_api_token, **ACCEPT_HEADER}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()


def upload(*, sodar_url, sodar_api_token, project_uuid, file_paths):
    """Upload and replace ISA-tab sample sheet to SODAR."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]
    url_tpl = "%(sodar_url)s/samplesheets/api/import/%(project_uuid)s"
    url = url_tpl % {"sodar_url": sodar_url, "project_uuid": project_uuid}

    logger.debug("HTTP POST request to %s", url)
    headers = {"Authorization": "Token %s" % sodar_api_token, **ACCEPT_HEADER}
    with contextlib.ExitStack() as stack:
        files = []
        for no, path in enumerate(file_paths):
            p = pathlib.Path(path)
            files.append(
                (
                    "file_%d" % no,
                    (p.name, stack.enter_context(p.open("rt")), "text/plain"),
                )
            )
        r = requests.post(url, headers=headers, files=files)
    r.raise_for_status()
    return r.json()
