"""Unit tests for the Ubuntu charm."""

from ops import testing

import charm


def _patch_hostname_fs(monkeypatch, tmp_path, initial_hostname: str = "original-host"):
    """Redirect the charm's hostname paths at a tmp filesystem seeded with initial_hostname."""
    etc_hostname = tmp_path / "etc-hostname"
    etc_hostname.write_text(f"{initial_hostname}\n")
    original_snapshot = tmp_path / "original-hostname"
    monkeypatch.setattr(charm, "HOSTNAME_PATH", etc_hostname)
    monkeypatch.setattr(charm, "ORIGINAL_HOSTNAME_PATH", original_snapshot)
    calls: list[list[str]] = []

    def record(cmd, *a, **kw):
        calls.append(cmd)

    monkeypatch.setattr("charm.subprocess.check_call", record)
    return etc_hostname, original_snapshot, calls


def test_version(monkeypatch) -> None:
    """The workload version is set from lsb_release during initial hooks."""
    ctx = testing.Context(charm.UbuntuCharm)
    monkeypatch.setattr("charm.subprocess.check_output", lambda *a, **kw: b"test\n")
    state_out = ctx.run(
        ctx.on.install(),
        testing.State(leader=True),
    )
    assert state_out.workload_version == "test"


def test_hostname(monkeypatch, tmp_path) -> None:
    """Setting hostname config updates /etc/hostname and snapshots the original."""
    etc_hostname, original_snapshot, calls = _patch_hostname_fs(monkeypatch, tmp_path)
    ctx = testing.Context(charm.UbuntuCharm)
    state_out = ctx.run(
        ctx.on.config_changed(),
        testing.State(leader=True, config={"hostname": "foo"}),
    )
    assert etc_hostname.read_text() == "foo"
    assert original_snapshot.read_text() == "original-host"
    assert calls == [["hostname", "foo"]]
    assert isinstance(state_out.unit_status, testing.UnknownStatus)


def test_hostname_reset_restores_original(monkeypatch, tmp_path) -> None:
    """Clearing the hostname config restores the pre-charm hostname."""
    etc_hostname, original_snapshot, calls = _patch_hostname_fs(monkeypatch, tmp_path)
    original_snapshot.parent.mkdir(parents=True, exist_ok=True)
    original_snapshot.write_text("original-host")
    etc_hostname.write_text("foo\n")

    ctx = testing.Context(charm.UbuntuCharm)
    ctx.run(
        ctx.on.config_changed(),
        testing.State(leader=True, config={"hostname": ""}),
    )
    assert etc_hostname.read_text() == "original-host"
    assert calls == [["hostname", "original-host"]]


def test_hostname_reset_without_snapshot_is_noop(monkeypatch, tmp_path) -> None:
    """Clearing the hostname config with no snapshot present is a no-op."""
    etc_hostname, original_snapshot, calls = _patch_hostname_fs(monkeypatch, tmp_path)
    ctx = testing.Context(charm.UbuntuCharm)
    ctx.run(
        ctx.on.config_changed(),
        testing.State(leader=True, config={"hostname": ""}),
    )
    assert etc_hostname.read_text() == "original-host\n"
    assert not original_snapshot.exists()
    assert calls == []


def test_charm_status(monkeypatch) -> None:
    """After install, the charm has active status."""
    ctx = testing.Context(charm.UbuntuCharm)
    monkeypatch.setattr("charm.subprocess.check_output", lambda *a, **kw: b"test\n")
    state_out = ctx.run(
        ctx.on.install(),
        testing.State(leader=True),
    )
    assert isinstance(state_out.unit_status, testing.ActiveStatus)
