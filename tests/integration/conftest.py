"""Session-scoped charm fixture for integration tests."""

import os
import pathlib

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


@pytest.fixture(scope="session")
def charm() -> pathlib.Path:
    """Return the path of the charm under test."""
    charm_path = os.environ.get("CHARM_PATH")
    if not charm_path:
        charm_dir = pathlib.Path()
        charm_path = next(charm_dir.glob("*.charm"))
    return pathlib.Path(charm_path).resolve()
