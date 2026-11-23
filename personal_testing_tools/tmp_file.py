"""Classes for temporary testing files."""

import os
import shutil
import tempfile
from collections.abc import Iterable
from typing import IO


class TmpFileInput:
    """Input values for temp testing files.

    :param name: File name
    :param content: File content
    :param expected: Asserted against the contents of the file on exit if provided"""

    __slots__ = ("content", "expected", "name")

    def __init__(
        self, name: str, content: bytes, expected: bytes | None = None
    ) -> None:
        self.name: str = name
        self.content: bytes = content
        self.expected: bytes | None = expected


class TmpFile:
    """A temporary file used for testing. Only usable as a context manager.
    Unlike builtin tempfile, this class does not keep the file open so it
    can be modified in the context.

    :param test_file: Check `TmpFileInput` for input details"""

    __slots__ = ("_test_file", "_tmp_file")

    def __init__(self, test_file: TmpFileInput) -> None:
        self._test_file: TmpFileInput = test_file
        self._tmp_file: IO[bytes]

    def __enter__(self) -> str:
        self._tmp_file = tempfile.NamedTemporaryFile(
            prefix=self._test_file.name, delete=False
        )

        try:
            try:
                self._tmp_file.write(self._test_file.content)
            finally:
                self._tmp_file.close()
        except OSError:
            self._clean_up()
            raise

        return self._tmp_file.name

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        if exc_type is None and self._test_file.expected is not None:
            with open(self._tmp_file.name, "rb") as fp:
                assert fp.read() == self._test_file.expected

        self._clean_up()

    def _clean_up(self) -> None:
        os.remove(self._tmp_file.name)


class TmpFileInDirInput(TmpFileInput):
    """Input values for testing files in a temp folder.

    :param name: File name
    :param content: File content
    :param expected: Asserted against the contents of the file on exit if provided
    :param rel_dir_path: The relative path of the parent dir if any"""

    __slots__ = ("rel_dir_path",)

    def __init__(
        self,
        name: str,
        content: bytes,
        expected: bytes | None = None,
        *,
        rel_dir_path: str = "",
    ) -> None:
        super().__init__(name, content, expected)

        self.rel_dir_path: str = rel_dir_path


class TmpDir:
    """A temporary folder used for testing. Only usable as a context manager.
    Unlike builtin tempfile, this class does not keep the files open so they
    can be modified in the context.

    :param test_file: Check `TmpFileInDirInput` for input details"""

    __slots__ = ("_temp_folder", "_test_files")

    def __init__(self, test_files: Iterable[TmpFileInDirInput]) -> None:
        self._test_files: Iterable[TmpFileInDirInput] = test_files
        self._temp_folder: tempfile.TemporaryDirectory

    def __enter__(self) -> str:
        self._temp_folder = tempfile.TemporaryDirectory(delete=False)

        try:
            for test_file in self._test_files:
                file_path: str = self._get_full_path(test_file)

                # Only need to makedirs if a relative dir path was provided
                if test_file.rel_dir_path:
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)

                with open(file_path, "wb") as fp:
                    fp.write(test_file.content)
        except OSError:
            self._clean_up()
            raise

        return self._temp_folder.name

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        if exc_type is None:
            for test_file in self._test_files:
                if test_file.expected is None:
                    continue

                with open(self._get_full_path(test_file), "rb") as fp:
                    assert fp.read() == test_file.expected

        self._clean_up()

    def _clean_up(self) -> None:
        shutil.rmtree(self._temp_folder.name)

    def _get_full_path(self, test_file: TmpFileInDirInput) -> str:
        return os.path.join(
            self._temp_folder.name, test_file.rel_dir_path, test_file.name
        )
