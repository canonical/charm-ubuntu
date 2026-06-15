"""Teach python-libjuju about Ubuntu series it does not yet ship with.

python-libjuju is no longer actively maintained and its hard-coded series
tables stop at 24.04 (noble). The deploy path in ``juju.utils`` looks up the
series name in ``UBUNTU_SERIES``/``ALL_SERIES_VERSIONS`` to derive the base
channel, so deploying ``resolute`` raises ``JujuError: Unknown series``
without this patch. Mutate the dicts in place (conftest loads before test
modules are collected) so ``from juju.utils import ALL_SERIES_VERSIONS`` in
``test_charm.py`` sees the new entries too.
"""

from juju import utils as _juju_utils

_EXTRA_UBUNTU_SERIES = {
    "resolute": "26.04",
}

for _series, _version in _EXTRA_UBUNTU_SERIES.items():
    _juju_utils.UBUNTU_SERIES.setdefault(_series, _version)
    _juju_utils.ALL_SERIES_VERSIONS.setdefault(_series, _version)
