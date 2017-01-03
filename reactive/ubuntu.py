
import subprocess

from charms.reactive import when, when_not, set_state
from charmhelpers.core.hookenv import status_set, application_version_set, config
from charmhelpers.core.host import lsb_release


@when_not('ubuntu.ready')
def status_ubuntu():
    status_set('active', 'ready')
    application_version_set(lsb_release()['DISTRIB_RELEASE'])
    set_state('ubuntu.ready')


@when('config.changed.hostname')
def update_hostname():
    hostname = config().get('hostname')
    if not hostname:
        return

    with open('/etc/hostname', 'w') as f:
        f.write(hostname)

    subprocess.check_call(['hostname', hostname])
