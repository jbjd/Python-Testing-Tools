"""Extensions for test marks."""

import sys
import unittest


def mark_platform_dependent(platform: str):  # noqa: ANN201
    """Convenience function to skip tests with unittest.skipIf
    that are platform dependent.

    :param platform: The only platform the test can run on"""
    return unittest.skipIf(sys.platform != platform, reason=f"Only runs on {platform}")


def mark_windows_only():  # noqa: ANN201
    """Convenience function to skip tests with unittest.skipIf
    that are only intended to run on Windows."""
    return mark_platform_dependent("win32")
