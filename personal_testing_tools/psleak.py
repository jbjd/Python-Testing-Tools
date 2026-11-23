"""Extensions for psleak."""

import os

from psleak import MemoryLeakTestCase


def _raise_if_bad_env_value(env_var: str, expected: str) -> None:
    """Raises if env value isn't set to `expected`.

    :param env_var: Environment variable to check
    :param expected: The expected value
    :raises ValueError: If value is unexpected"""

    if os.environ.get(env_var) != expected:
        raise ValueError(
            f"Need to set env variable {env_var}={expected} for psleak to work properly"
        )


class MemoryLeakTestCaseExt(MemoryLeakTestCase):
    """Subclasses `MemoryLeakTestCase` with checks that
    important python configs are set."""

    def setUp(self) -> None:
        _raise_if_bad_env_value("PYTHONMALLOC", "malloc")
        _raise_if_bad_env_value("PYTHONUNBUFFERED", "1")
