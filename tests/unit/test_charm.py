import inspect
from pathlib import Path
from unittest import TestCase, mock

import yaml
from ops.testing import Harness

import charm


def charm_config() -> str:
    """Return the charm configuration as a string readfrom charmcraft.yaml."""
    filename = inspect.getfile(charm.UbuntuCharm)
    charm_dir = Path(filename).parents[1]
    content = (charm_dir / "charmcraft.yaml").read_text()
    config = yaml.safe_load(content)["config"]
    return yaml.safe_dump(config)


class TestCharm(TestCase):
    """Ubuntu charm unit tests."""

    @classmethod
    def setUpClass(cls):
        cls.pPath = mock.patch("charm.Path")
        cls.mPath = cls.pPath.start()

        cls.pcheck_call = mock.patch("charm.check_call")
        cls.mcheck_call = cls.pcheck_call.start()

        cls.pcheck_output = mock.patch("charm.check_output")
        cls.mcheck_output = cls.pcheck_output.start()
        cls.mcheck_output.return_value = b"test\n"

        cls.harness = Harness(charm.UbuntuCharm, config=charm_config())
        cls.harness.set_leader(is_leader=True)
        cls.harness.begin_with_initial_hooks()

    @classmethod
    def tearDownClass(cls):
        cls.pcheck_output.stop()
        cls.pcheck_call.stop()
        cls.pPath.stop()

    def test_version(self):
        # Set during cls.harness.begin_with_initial_hooks()
        assert self.harness.get_workload_version() == "test"

    def test_hostname(self):
        self.harness.update_config({"hostname": "foo"})
        self.mPath.assert_called_with("/etc/hostname")
        self.mPath().write_text.assert_called_once_with("foo")
        self.mcheck_call.assert_called_once_with(["hostname", "foo"])
