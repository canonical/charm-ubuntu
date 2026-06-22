"""Unit tests for the Ubuntu charm."""

import inspect
from pathlib import Path
from unittest import mock

import ops.testing
import pytest
import yaml
from ops.testing import Harness

import charm

ops.testing.SIMULATE_CAN_CONNECT = True


def charm_config() -> str:
    """Return the charm configuration as a string read from charmcraft.yaml."""
    filename = inspect.getfile(charm.UbuntuCharm)
    charm_dir = Path(filename).parents[1]
    content = (charm_dir / "charmcraft.yaml").read_text()
    config = yaml.safe_load(content)["config"]
    return yaml.safe_dump(config)


@pytest.fixture()
def harness() -> Harness:
    """Create a Harness with the charm config and leader status."""
    with (
        mock.patch("charm.Path"),
        mock.patch("charm.check_call"),
        mock.patch("charm.check_output", return_value=b"test\n"),
    ):
        h = Harness(charm.UbuntuCharm, config=charm_config())
        h.set_leader(is_leader=True)
        h.begin_with_initial_hooks()
        yield h
        h.cleanup()


class TestCharm:
    """Ubuntu charm unit tests."""

    def test_version(self, harness: Harness) -> None:
        """The workload version is set from lsb_release during initial hooks."""
        assert harness.get_workload_version() == "test"

    def test_hostname(self, harness: Harness, monkeypatch: pytest.MonkeyPatch) -> None:
        """Setting hostname config updates /etc/hostname and calls hostname."""
        mock_path = mock.MagicMock(spec=Path)
        mock_check_call = mock.MagicMock()
        monkeypatch.setattr("charm.Path", mock_path)
        monkeypatch.setattr("charm.check_call", mock_check_call)

        harness.update_config({"hostname": "foo"})

        mock_path.assert_called_with("/etc/hostname")
        mock_path.return_value.write_text.assert_called_once_with("foo")
        mock_check_call.assert_called_once_with(["hostname", "foo"])

    def test_charm_ready(self, harness: Harness) -> None:
        """The unit status message indicates the charm is ready."""
        prefixes = ["ready", "Ready", "Unit is ready"]
        assert harness.model.unit.status.message in prefixes
