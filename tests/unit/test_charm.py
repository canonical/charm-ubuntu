"""Unit tests for the Ubuntu charm."""

import pathlib

from ops import testing

import charm


def test_version(monkeypatch) -> None:
    """The workload version is set from lsb_release during initial hooks."""
    ctx = testing.Context(charm.UbuntuCharm)
    monkeypatch.setattr("charm.subprocess.check_output", lambda *a, **kw: b"test\n")
    state_out = ctx.run(
        ctx.on.install(),
        testing.State(leader=True),
    )
    assert state_out.workload_version == "test"


def test_hostname(monkeypatch) -> None:
    """Setting hostname config updates /etc/hostname and calls hostname."""
    ctx = testing.Context(charm.UbuntuCharm)
    original_write_text = pathlib.Path.write_text

    def mock_write_text(self, *args, **kwargs):
        if str(self) == "/etc/hostname":
            return None
        return original_write_text(self, *args, **kwargs)

    monkeypatch.setattr(pathlib.Path, "write_text", mock_write_text)
    monkeypatch.setattr("charm.subprocess.check_call", lambda *a, **kw: None)
    state_out = ctx.run(
        ctx.on.config_changed(),
        testing.State(leader=True, config={"hostname": "foo"}),
    )
    assert isinstance(state_out.unit_status, testing.ActiveStatus)


def test_charm_status(monkeypatch) -> None:
    """After install, the charm has active status."""
    ctx = testing.Context(charm.UbuntuCharm)
    monkeypatch.setattr("charm.subprocess.check_output", lambda *a, **kw: b"test\n")
    state_out = ctx.run(
        ctx.on.install(),
        testing.State(leader=True),
    )
    assert isinstance(state_out.unit_status, testing.ActiveStatus)
