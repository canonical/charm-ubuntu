#!/usr/bin/python3
"""
Ubuntu charm functional test.  Take note that the Ubuntu
charm does not have any relations or config options
to exercise.
"""

import amulet
from charmhelpers.contrib.amulet.utils import AmuletUtils
import logging


def ubuntu_basic_deployment(series):
    """ Common test routines to run per-series. """

    # Initialize
    seconds = 900
    u = AmuletUtils(logging.DEBUG)
    d = amulet.Deployment(series=series)
    d.add('ubuntu')

    # Deploy services, wait for started state.  Fail or skip on timeout.
    try:
        d.setup(timeout=seconds)
        sentry_unit = d.sentry['ubuntu'][0]
    except amulet.helpers.TimeoutError:
        message = 'Deployment timed out ({}s)'.format(seconds)
        amulet.raise_status(amulet.FAIL, msg=message)
    except:
        raise

    # Confirm Ubuntu release name from the unit.
    release, ret = u.get_ubuntu_release_from_sentry(sentry_unit)
    if ret:
        # Something went wrong trying to query the unit, or it is an
        # unknown/alien release name based on distro-info validation.
        amulet.raise_status(amulet.FAIL, msg=ret)

    if release == series:
        u.log.info('Release/series check:  OK')
    else:
        msg = 'Release/series check:  FAIL ({} != {})'.format(release, series)
        u.log.error(msg)
        amulet.raise_status(amulet.FAIL, msg=msg)
