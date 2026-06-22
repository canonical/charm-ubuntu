#!/usr/bin/env python3

"""Ubuntu machine charm.

Deploys a pristine Ubuntu cloud/server image and optionally sets the hostname.
"""

import logging
import pathlib
import subprocess

import ops


logger = logging.getLogger(__name__)


class UbuntuCharm(ops.CharmBase):
    """Charm that deploys a pristine Ubuntu cloud/server image."""

    def __init__(self, framework: ops.Framework) -> None:
        """Initialize charm and register event observers."""
        super().__init__(framework)

        framework.observe(self.on.install, self._set_version)
        framework.observe(self.on.leader_elected, self._set_version)
        framework.observe(self.on.upgrade_charm, self._set_version)
        framework.observe(self.on.config_changed, self._update_hostname)

    def _set_version(self, event: ops.EventBase) -> None:
        """Set application version to the Ubuntu release on the leader unit."""
        self.unit.status = ops.ActiveStatus("ready")
        if not self.unit.is_leader():
            return
        try:
            output = subprocess.check_output(["lsb_release", "-r", "-s"])
            version = output.decode("utf8").strip()
            self.unit.set_workload_version(version)
        except Exception:
            logger.exception("Error getting release")

    def _update_hostname(self, event: ops.ConfigChangedEvent) -> None:
        """Update the machine hostname based on the config option."""
        hostname = self.config["hostname"]
        if not hostname:
            return

        pathlib.Path("/etc/hostname").write_text(hostname)
        subprocess.check_call(["hostname", hostname])
        self.unit.status = ops.ActiveStatus("ready")


if __name__ == "__main__":
    ops.main(UbuntuCharm)
