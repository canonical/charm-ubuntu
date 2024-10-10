import logging
from pathlib import Path

import pytest
import yaml
from juju.utils import ALL_SERIES_VERSIONS


log = logging.getLogger(__name__)
meta = yaml.safe_load(Path("charmcraft.yaml").read_text())
CHANNEL_TO_SERIES = dict(reversed(mapping) for mapping in ALL_SERIES_VERSIONS.items())
CHARM_SUPPORT = {
    CHANNEL_TO_SERIES[base["channel"]]: base["channel"]
    for base in meta["bases"][0]["run-on"]
}


@pytest.mark.abort_on_fail
async def test_build_and_deploy(ops_test):
    charm = await ops_test.build_charm(".")
    for series in CHARM_SUPPORT:
        await ops_test.model.deploy(charm, application_name=series, series=series)
    await ops_test.model.wait_for_idle(wait_for_active=True, timeout=60 * 60)


async def test_app_versions(ops_test):
    """Validate that the app versions are correct."""
    for series, expected in CHARM_SUPPORT.items():
        app = ops_test.model.applications[series]
        assert app.workload_version == expected
