.. image:: https://github.com/bihealth/sodar-cli/workflows/CI/badge.svg
    :target: https://github.com/bihealth/sodar-cli/actions
    :alt: Continuous Integration Status
.. image:: https://app.codacy.com/project/badge/Grade/0bf5c6d8a91e4a7380676672e466525d
    :target: https://www.codacy.com/gh/bihealth/sodar-cli/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bihealth/sodar-cli&amp;utm_campaign=Badge_Grade
.. image:: https://app.codacy.com/project/badge/Coverage/0bf5c6d8a91e4a7380676672e466525d
    :target: https://www.codacy.com/gh/bihealth/sodar-cli/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bihealth/sodar-cli&amp;utm_campaign=Badge_Coverage
.. image:: https://coveralls.io/repos/github/bihealth/sodar-cli/badge.svg?branch=main
    :target: https://coveralls.io/github/bihealth/sodar-cli?branch=main
.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :alt: MIT License
    :target: https://opensource.org/licenses/MIT

=========
SODAR CLI
=========

Command line interface for `SODAR Server <https://github.com/bihealth/sodar-server>`__.

---------------
Getting Started
---------------

- `SODAR Homepage <https://www.cubi.bihealth.org/software/sodar/>`__
- `Manual <https://sodar-server.readthedocs.io/en/latest/>`__

--------------------
SODAR Repositories
--------------------

`sodar-server <https://github.com/bihealth/sodar-server>`__
    SODAR web server for meta and mass data management.
`sodar-taskflow <https://github.com/bihealth/sodar-taskflow>`__
    Helper component for running tasks with rollback functionality.

------------
Installation
------------

.. code-block:: bash

    $ git clone git@github.com:bihealth/sodar-cli.git
    $ cd sodar-cli
    $ conda create -n sodar-cli python=3.7
    $ conda activate sodar-cli
    $ pip install -e .
    $ cat >~/.sodarrc.toml <<EOF
    [global]

    # URL to SODAR server.
    sodar_server_url = "https://sodar.example.com/"
    # API token to use for SODAR API.
    sodar_api_token = "XXX"
    EOF

---------
Releasing
---------

.. code-block:: bash

    $ $EDITOR HISTORY.rst
    $ git tag ...
    $ rm -rf dist
    $ python setup.py sdist
    $ twine upload dist/*.tar.gz
