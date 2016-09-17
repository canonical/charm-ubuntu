
from charms.reactive import when_not, set_state
from charmhelpers.core.hookenv import status_set, application_version_set
from charmhelpers.core.host import lsb_release


@when_not('ubuntu.ready')
def status_ubuntu():
    status_set('active', 'ready')
    application_version_set(lsb_release()['DISTRIB_RELEASE'])
    set_state('ubuntu.ready')
