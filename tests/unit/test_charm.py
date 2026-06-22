"""Unit tests for the Ubuntu charm."""

from unittest import mock

from ops import testing

import charm


def test_version() -> None:
    """The workload version is set from lsb_release during initial hooks."""
    ctx = testing.Context(charm.UbuntuCharm)
    with (
        mock.patch("charm.subprocess.check_output", return_value=b"test\n"),
    ):
        state_out = ctx.run(
            ctx.on.install(),
            testing.State(leader=True),
        )
    assert state_out.workload_version == "test"


def test_hostname() -> None:
    """Setting hostname config updates /etc/hostname and calls hostname."""
    ctx = testing.Context(charm.UbuntuCharm)
    with (
        mock.patch("charm.pathlib.Path"),
        mock.patch("charm.subprocess.check_call"),
        mock.patch("charm.subprocess.check_output", return_value=b"test\n"),
    ):
        state_out = ctx.run(
            ctx.on.config_changed(),
            testing.State(leader=True, config={"hostname": "foo"}),
        )
    assert state_out.unit_status == testing.ActiveStatus("ready")


def test_charm_ready() -> None:
    """The unit status message indicates the charm is ready."""
    ctx = testing.Context(charm.UbuntuCharm)
    with (
        mock.patch("charm.subprocess.check_output", return_value=b"test\n"),
    ):
        state_out = ctx.run(
            ctx.on.install(),
            testing.State(leader=True),
        )
    assert state_out.unit_status == testing.ActiveStatus("ready")
