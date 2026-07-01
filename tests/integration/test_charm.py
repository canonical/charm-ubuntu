"""Integration tests for the Ubuntu charm."""

import os
import pathlib

import jubilant
import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add integration test options."""
    parser.addoption(
        "--base",
        action="store",
        default=None,
        help="Ubuntu base to deploy (e.g. 22.04)",
    )


@pytest.fixture(scope="session")
def base(request: pytest.FixtureRequest) -> str | None:
    """Return the Ubuntu base to deploy on (e.g. '22.04'), or None for default."""
    return request.config.getoption("--base") or os.environ.get("BASE")


@pytest.mark.juju_setup
def test_build_and_deploy(charm: pathlib.Path, juju: jubilant.Juju, base: str | None) -> None:
    """Deploy the charm and verify it goes to active status."""
    kwargs = {}
    if base:
        kwargs["base"] = f"ubuntu@{base}"
    juju.deploy(charm, "ubuntu", **kwargs)
    juju.wait(jubilant.all_active, timeout=60 * 60)


def test_app_versions(charm: pathlib.Path, juju: jubilant.Juju) -> None:
    """Validate that the app version is set correctly."""
    status = juju.wait(jubilant.all_active)
    app = status.apps["ubuntu"]
    assert app.version is not None
