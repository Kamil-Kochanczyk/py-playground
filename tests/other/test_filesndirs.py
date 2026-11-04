from pathlib import Path

import pytest

from py_playground.other.filesndirs import is_safe_archive_member


@pytest.mark.parametrize(
    "member_name",
    [
        "report.txt",
        "nested/report.txt",
        "nested/./report.txt",
    ],
)
def test_is_safe_archive_member_accepts_paths_inside_destination(tmp_path: Path, member_name: str) -> None:
    assert is_safe_archive_member(member_name, tmp_path)


@pytest.mark.parametrize(
    "member_name",
    [
        "../outside.txt",
        "nested/../../outside.txt",
        "/outside.txt",
        r"..\outside.txt",
        r"C:\outside.txt",
        r"\\server\share\outside.txt",
        "",
    ],
)
def test_is_safe_archive_member_rejects_paths_outside_destination(tmp_path: Path, member_name: str) -> None:
    assert not is_safe_archive_member(member_name, tmp_path)
