import logging
from pathlib import Path

import pytest
import yaml
from pytest_operator import OperatorTest


log = logging.getLogger(__name__)


class UbuntuIntegrationTest(OperatorTest):
    meta = yaml.safe_load(Path("metadata.yaml").read_text())

    @pytest.mark.order("first")
    @pytest.mark.abort_on_fail
    async def test_build_and_deploy(self):
        charm = await self.build_charm(".")
        for series in self.meta["series"]:
            await self.model.deploy(charm, application_name=series, series=series)
        await self.model.wait_for_idle(wait_for_active=True, timeout=60 * 60)

    async def test_app_versions(self):
        """ Validate that the app versions are correct. """
        expected = {
            "focal": "20.04",
            "bionic": "18.04",
            "xenial": "16.04",
            "groovy": "20.10",
        }
        for series in self.meta["series"]:
            app = self.model.applications[series]
            assert app.workload_version == expected[series]
