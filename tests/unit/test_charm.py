from unittest import TestCase, mock

from ops.testing import Harness

import charm


class TestCharm(TestCase):
    """Ubuntu charm unit tests."""

    @classmethod
    def setUpClass(cls):
        cls.pPath = mock.patch("charm.Path")
        cls.mPath = cls.pPath.start()
        cls.mPath().read_text.return_value = "DISTRIB_RELEASE = test\n"

        cls.pcheck_call = mock.patch("subprocess.check_call")
        cls.mcheck_call = cls.pcheck_call.start()

        cls.harness = Harness(charm.UbuntuCharm)
        cls.harness.set_leader(is_leader=True)
        cls.harness.begin()

    @classmethod
    def tearDownClass(cls):
        cls.pcheck_call.stop()
        cls.pPath.stop()

    def test_version(self):
        # Set during cls.harness.begin()
        assert self.harness.get_workload_version() == "test"

    def test_hostname(self):
        self.harness.update_config({"hostname": "foo"})
        self.mPath.assert_called_with("/etc/hostname")
        self.mPath().write_text.assert_called_once_with("foo")
        self.mcheck_call.assert_called_once_with(["hostname", "foo"])
