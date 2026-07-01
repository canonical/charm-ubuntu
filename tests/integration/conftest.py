"""Session-scoped charm fixture for integration tests."""

import os
import pathlib

import pytest


@pytest.fixture(scope="session")
def charm() -> pathlib.Path:
    """Return the path of the charm under test."""
    charm_path = os.environ.get("CHARM_PATH")
    if not charm_path:
        charm_dir = pathlib.Path()
        charm_path = next(charm_dir.glob("*.charm"))
    return pathlib.Path(charm_path)
