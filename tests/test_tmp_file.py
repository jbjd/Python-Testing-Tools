"""Tests for tmp_file module."""

import os

import pytest

from personal_testing_tools.tmp_file import (
    TmpDir,
    TmpFile,
    TmpFileInDirInput,
    TmpFileInput,
)


def test_tmp_file():
    """Should be tempoary."""

    tmp_input = TmpFileInput("asdf.txt", b"asdf")

    with TmpFile(tmp_input) as file:
        assert os.path.isfile(file)

    assert not os.path.exists(file)


def test_tmp_file_assert():
    """Should assert if expected value provided."""

    tmp_input = TmpFileInput("asdf.txt", b"asdf", b"asdf")

    with TmpFile(tmp_input):
        pass  # all good, contents match

    tmp_input.expected = b"foo"

    with pytest.raises(AssertionError):  # noqa: SIM117
        with TmpFile(tmp_input):
            pass


def test_tmp_dir():
    """Should be tempoary."""

    name: str = "asdf.txt"
    deep_path: str = "a/b/c"
    tmp_input1 = TmpFileInDirInput(name, b"foo", rel_dir_path=deep_path)
    tmp_input2 = TmpFileInDirInput(name, b"bar")

    with TmpDir([tmp_input1, tmp_input2]) as folder:
        assert os.path.isdir(folder)
        assert os.path.isfile(os.path.join(folder, deep_path, name))
        assert os.path.isfile(os.path.join(folder, name))

    assert not os.path.exists(folder)


def test_tmp_dir_assert():
    """Should assert if expected value provided."""

    tmp_inputs = [TmpFileInDirInput("asdf.txt", b"bar", b"bar")]

    with TmpDir(tmp_inputs):
        pass  # all good, contents match

    tmp_inputs[0].expected = b"foo"

    with pytest.raises(AssertionError):  # noqa: SIM117
        with TmpDir(tmp_inputs):
            pass
