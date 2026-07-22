"""Integration tests for the Ubuntu charm."""

import pathlib
import platform

import jubilant
import pytest

_ARCH_MAP = {"x86_64": "amd64", "aarch64": "arm64", "ppc64le": "ppc64el", "s390x": "s390x"}


@pytest.mark.juju_setup
def test_build_and_deploy(charm: pathlib.Path, juju: jubilant.Juju) -> None:
    """Deploy the charm and verify it goes to active status."""
    arch = _ARCH_MAP.get(platform.machine(), platform.machine())
    juju.deploy(charm, "ubuntu", constraints={"arch": arch})
    juju.wait(jubilant.all_active, timeout=60 * 60)


def test_app_versions(charm: pathlib.Path, juju: jubilant.Juju) -> None:
    """Validate that the app version is set correctly."""
    status = juju.wait(jubilant.all_active)
    app = status.apps["ubuntu"]
    assert app.version is not None
