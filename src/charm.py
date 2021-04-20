#!/usr/bin/env python3

import logging
from pathlib import Path
from subprocess import check_call, check_output

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus


log = logging.getLogger(__name__)


class UbuntuCharm(CharmBase):
    def __init__(self, *args):
        """Initialize charm.

        Setup hook event observers and any other basic initialization.
        """
        super().__init__(*args)

        for event in (
            self.on.install,
            self.on.leader_elected,
            self.on.upgrade_charm,
            self.on.post_series_upgrade,
        ):
            self.framework.observe(event, self._set_version)
        self.framework.observe(self.on.config_changed, self._update_hostname)

    def _set_version(self, _):
        """Set application version.

        Invoked for relevant hook events and, on the leader unit, determine and
        set the application-level workload version to the Ubuntu version upon
        which the charm is running.
        """
        self.unit.status = ActiveStatus(message="Ready")
        if not self.unit.is_leader():
            return
        try:
            output = check_output(["lsb_release", "-r", "-s"])
            version = output.decode("utf8").strip()
            self.unit.set_workload_version(version)
        except Exception:
            log.exception("Error getting release")

    def _update_hostname(self, event):
        """Update the machine hostname based on the config option."""
        hostname = self.config["hostname"]
        if not hostname:
            return

        Path("/etc/hostname").write_text(hostname)
        check_call(["hostname", hostname])


if __name__ == "__main__":
    main(UbuntuCharm)
