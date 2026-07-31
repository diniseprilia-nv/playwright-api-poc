"""Test entry for create_route.feature."""

from pathlib import Path

from pytest_bdd import scenarios

from tests.route.steps import routing_steps  # noqa: F401

scenarios(Path(__file__).resolve().parent.parent / "features" / "create_route.feature")
