"""Integration tests for the Ubuntu charm."""

import pathlib

import jubilant
import pytest


@pytest.mark.juju_setup
def test_build_and_deploy(charm: pathlib.Path, juju: jubilant.Juju) -> None:
    """Deploy the charm and verify it goes to active status."""
    import platform
    import zipfile

    print(f"[diag] charm path: {charm}", flush=True)
    print(f"[diag] platform.machine(): {platform.machine()}", flush=True)
    with zipfile.ZipFile(charm) as z:
        print(f"[diag] manifest.yaml:\n{z.read('manifest.yaml').decode()}", flush=True)
    print("[diag] juju model-defaults:", flush=True)
    print(juju.cli("model-defaults", "--format=yaml", include_model=False), flush=True)
    print("[diag] juju constraints (controller):", flush=True)
    print(juju.cli("constraints", include_model=False), flush=True)
    print("[diag] juju controller-config:", flush=True)
    print(juju.cli("controller-config", "--format=yaml", include_model=False), flush=True)
    juju.deploy(charm, "ubuntu")
    juju.wait(jubilant.all_active, timeout=60 * 60)


def test_app_versions(charm: pathlib.Path, juju: jubilant.Juju) -> None:
    """Validate that the app version is set correctly."""
    status = juju.wait(jubilant.all_active)
    app = status.apps["ubuntu"]
    assert app.version is not None
