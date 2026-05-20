"""Smoke test for ADM CLI."""

from adm_cli import app


def test_app_exists():
    assert app is not None
    assert app.info.name == "adm"
