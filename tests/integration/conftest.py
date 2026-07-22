"""Session-scoped charm fixture for integration tests."""

from __future__ import annotations

import os
import pathlib
from typing import Protocol

import pytest


class _CharmPaths(Protocol):
    """The subset of opcli's ``CharmPathList`` that we rely on."""

    def __getitem__(self, base: str) -> str: ...


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
def charm(charm_paths: dict[str, _CharmPaths], base: str | None) -> pathlib.Path:
    """Return the path of the charm under test."""
    resolved_base = base or "24.04"
    return pathlib.Path(charm_paths["ubuntu"][f"ubuntu@{resolved_base}"]).resolve()
