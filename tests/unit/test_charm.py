from unittest import TestCase, mock

from ops.testing import Harness

import charm


class TestCharm(TestCase):
    """Ubuntu charm unit tests."""

    @classmethod
    def setUpClass(cls):
        pPath = mock.patch("charm.Path")
        cls.mPath = pPath.start()
        cls.addClassCleanup(pPath.stop)
        cls.mPath().read_text.return_value = "DISTRIB_RELEASE = test\n"

        pcheck_call = mock.patch("subprocess.check_call")
        cls.mcheck_call = pcheck_call.start()
        cls.addClassCleanup(pcheck_call.stop)

        cls.harness = Harness(charm.UbuntuCharm)
        cls.harness.set_leader(is_leader=True)
        cls.harness.begin()

    def test_version(self):
        # Set during cls.harness.begin()
        assert self.harness.get_workload_version() == "test"

    def test_hostname(self):
        self.harness.update_config({"hostname": "foo"})
        self.mPath.assert_called_with("/etc/hostname")
        self.mPath().write_text.assert_called_once_with("foo")
        self.mcheck_call.assert_called_once_with(["hostname", "foo"])
