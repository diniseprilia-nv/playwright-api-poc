"""Test entry for create_order.feature."""

from pathlib import Path

from pytest_bdd import scenarios

from tests.order.steps import ordering_steps  # noqa: F401

scenarios(Path(__file__).resolve().parent.parent / "features" / "create_order.feature")
