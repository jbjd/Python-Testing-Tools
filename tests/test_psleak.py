"""Tests for psleak extensions."""

import os

import pytest

from personal_testing_tools.psleak import MemoryLeakTestCaseExt


class TempEnvVars:
    """Temporarily sets the env vars to desired values to test psleak extensions."""

    __slots__ = ("_buffered_fake", "_buffered_real", "_malloc_fake", "_malloc_real")

    def __init__(self, malloc: str, buffered: str) -> None:
        self._malloc_fake: str = malloc
        self._buffered_fake: str = buffered

    def __enter__(self) -> None:
        self._malloc_real = os.environ.get("PYTHONMALLOC")
        self._buffered_real = os.environ.get("PYTHONUNBUFFERED")

        os.environ["PYTHONMALLOC"] = self._malloc_fake
        os.environ["PYTHONUNBUFFERED"] = self._buffered_fake

    def __exit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001

        self._reset_env_var("PYTHONMALLOC", self._malloc_real)
        self._reset_env_var("PYTHONUNBUFFERED", self._buffered_real)

    @staticmethod
    def _reset_env_var(env_var: str, value: str | None) -> None:
        if value is not None:
            os.environ[env_var] = value
        else:
            del os.environ[env_var]


def test_errors_on_bad_env():
    """Should raise ValueError on bad env values."""
    test_case = MemoryLeakTestCaseExt()

    with TempEnvVars("asdf", "1"):  # noqa: SIM117
        with pytest.raises(ValueError):
            test_case.setUp()

    with TempEnvVars("malloc", "0"):  # noqa: SIM117
        with pytest.raises(ValueError):
            test_case.setUp()


def test_no_error_on_good_env():
    """Should not raise ValueError on good env values."""
    test_case = MemoryLeakTestCaseExt()

    with TempEnvVars("malloc", "1"):
        test_case.setUp()
