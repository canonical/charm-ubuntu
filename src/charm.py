#!/usr/bin/env python3

"""Ubuntu machine charm.

Deploys a pristine Ubuntu cloud/server image and optionally sets the hostname.
"""

import logging
import pathlib
import subprocess

import ops

logger = logging.getLogger(__name__)

HOSTNAME_PATH = pathlib.Path("/etc/hostname")
ORIGINAL_HOSTNAME_PATH = pathlib.Path("/var/lib/charm-ubuntu/original-hostname")


class UbuntuCharm(ops.CharmBase):
    """Charm that deploys a pristine Ubuntu cloud/server image."""

    def __init__(self, framework: ops.Framework):
        """Initialise the charm and register event observers."""
        super().__init__(framework)

        framework.observe(self.on.install, self._set_version)
        framework.observe(self.on.leader_elected, self._set_version)
        framework.observe(self.on.upgrade_charm, self._set_version)
        framework.observe(self.on.config_changed, self._update_hostname)

    def _set_version(self, event: ops.EventBase) -> None:
        """Set application version to the Ubuntu release on the leader unit."""
        self.unit.status = ops.ActiveStatus()
        if not self.unit.is_leader():
            return
        try:
            output = subprocess.check_output(["lsb_release", "-r", "-s"])  # noqa: S607
            version = output.decode("utf8").strip()
            self.unit.set_workload_version(version)
        except Exception:
            logger.exception("Error getting release")

    def _update_hostname(self, event: ops.ConfigChangedEvent) -> None:
        """Update the machine hostname based on the config option.

        Snapshots the pre-charm hostname on first use so that clearing the
        config option restores it.
        """
        configured = self.config.get("hostname")
        configured = configured if isinstance(configured, str) and configured else None

        if configured is None and not ORIGINAL_HOSTNAME_PATH.exists():
            return

        current = HOSTNAME_PATH.read_text().strip()
        if configured is not None and not ORIGINAL_HOSTNAME_PATH.exists():
            ORIGINAL_HOSTNAME_PATH.parent.mkdir(parents=True, exist_ok=True)
            ORIGINAL_HOSTNAME_PATH.write_text(current)

        if configured is not None:
            target = configured
        else:
            target = ORIGINAL_HOSTNAME_PATH.read_text().strip()
        if target == current:
            return
        HOSTNAME_PATH.write_text(target)
        subprocess.check_call(["hostname", target])  # noqa: S603, S607


if __name__ == "__main__":
    ops.main(UbuntuCharm)
