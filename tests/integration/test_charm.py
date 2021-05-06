import logging
from pathlib import Path

import pytest
import yaml


log = logging.getLogger(__name__)
meta = yaml.safe_load(Path("metadata.yaml").read_text())


@pytest.mark.abort_on_fail
async def test_build_and_deploy(ops_test):
    charm = await ops_test.build_charm(".")
    for series in meta["series"]:
        await ops_test.model.deploy(charm, application_name=series, series=series)
    await ops_test.model.wait_for_idle(wait_for_active=True, timeout=60 * 60)


async def test_app_versions(ops_test):
    """ Validate that the app versions are correct. """
    expected = {
        "focal": "20.04",
        "bionic": "18.04",
        "xenial": "16.04",
        "groovy": "20.10",
        "hirsute": "21.04",
    }
    for series in meta["series"]:
        app = ops_test.model.applications[series]
        assert app.workload_version == expected[series]
