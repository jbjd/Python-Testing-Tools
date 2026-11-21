"""Tests for tmp_file module."""

import os

from personal_testing_tools.tmp_file import TmpFile, TmpFileInput


def test_tmp_file():
    """Should be tempoary."""

    tmp_input = TmpFileInput("asdf.txt", b"asdf")

    with TmpFile(tmp_input) as file:
        pass

    assert not os.path.exists(file)
