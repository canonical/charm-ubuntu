#!/usr/bin/env python3

"""Ubuntu machine charm.

Deploys a pristine Ubuntu cloud/server image and optionally sets the hostname.
"""

import logging
from pathlib import Path
from subprocess import check_call, check_output

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus, MaintenanceStatus

logger = logging.getLogger(__name__)


class UbuntuCharm(CharmBase):
    """Charm that deploys a pristine Ubuntu cloud/server image."""

    def __init__(self, *args: object) -> None:
        """Initialize charm and register event observers."""
        super().__init__(*args)

        self.framework.observe(self.on.install, self._set_version)
        self.framework.observe(self.on.leader_elected, self._set_version)
        self.framework.observe(self.on.upgrade_charm, self._set_version)
        self.framework.observe(self.on.config_changed, self._update_hostname)

    def _set_version(self, _: object) -> None:
        """Set application version to the Ubuntu release on the leader unit."""
        self.unit.status = ActiveStatus("ready")
        if not self.unit.is_leader():
            return
        try:
            output = check_output(["lsb_release", "-r", "-s"])
            version = output.decode("utf8").strip()
            self.unit.set_workload_version(version)
        except Exception:
            logger.exception("Error getting release")

    def _update_hostname(self, _: object) -> None:
        """Update the machine hostname based on the config option."""
        hostname = self.config["hostname"]
        if not hostname:
            return

        self.unit.status = MaintenanceStatus(f"setting hostname to {hostname}")
        Path("/etc/hostname").write_text(hostname)
        check_call(["hostname", hostname])
        self.unit.status = ActiveStatus("ready")


if __name__ == "__main__":
    main(UbuntuCharm)
