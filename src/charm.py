#!/usr/bin/env python3

import logging
import subprocess
from pathlib import Path

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus


log = logging.getLogger(__name__)


class UbuntuCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)

        self.framework.observe(self.on.config_changed, self.on_config_changed)

        if self.unit.is_leader():
            self.set_version()

        self.unit.status = ActiveStatus()

    def set_version(self):
        try:
            for line in Path("/etc/lsb-release").read_text().splitlines():
                k, v = line.strip().split("=")
                if k.strip() == "DISTRIB_RELEASE":
                    self.unit.set_workload_version(v.strip())
        except Exception:
            log.exception("Error getting release")

    def on_config_changed(self, event):
        hostname = self.config["hostname"]
        if not hostname:
            return

        Path("/etc/hostname").write_text(hostname)
        subprocess.check_call(["hostname", hostname])


if __name__ == "__main__":
    main(UbuntuCharm)
