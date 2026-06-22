"""Integration tests for the Ubuntu charm."""

import pathlib

import jubilant
import pytest


@pytest.mark.juju_setup
def test_build_and_deploy(charm: pathlib.Path, juju: jubilant.Juju) -> None:
    """Deploy the charm and verify it goes to active status."""
    juju.deploy(charm, "ubuntu")
    juju.wait(jubilant.all_active, timeout=60 * 60)


def test_app_versions(charm: pathlib.Path, juju: jubilant.Juju) -> None:
    """Validate that the app version is set correctly."""
    status = juju.wait(jubilant.all_active)
    app = status.apps["ubuntu"]
    assert app.workload_version is not None
