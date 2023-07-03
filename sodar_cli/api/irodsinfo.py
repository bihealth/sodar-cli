from logzero import logger
import requests


def retrieve(*, sodar_url, sodar_api_token):
    """Get iRODS environment information."""
    while sodar_url.endswith("/"):
        sodar_url = sodar_url[:-1]
    url = f"{sodar_url}/irods/api/environment"

    logger.debug("HTTP GET request to %s", url)
    headers = {"Authorization": f"Token {sodar_api_token}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()
