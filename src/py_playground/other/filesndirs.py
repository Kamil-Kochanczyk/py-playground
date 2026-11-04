import contextlib
import csv
import datetime as dt
import os
import pickle
import random
import shutil
import stat
import string
import zipfile
from pathlib import Path, PurePosixPath, PureWindowsPath
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Literal, NamedTuple

import requests
from dotenv import load_dotenv
from pydantic import BaseModel

type ICSV = Literal["i"]
type SCSV = Literal["s"]


class FieldNamesCSV(NamedTuple):
    f1: ICSV
    f2: SCSV


class DataCSV(BaseModel):
    i: int
    s: str


def is_safe_archive_member(member_name: str, destination: Path) -> bool:
    """Return whether a ZIP member resolves inside the extraction destination.

    This validates a member path; it does not make a later unsafe extraction safe.

    Args:
        member_name (str): File inside an archive.
        destination (Path): Where the archive should be extracted.

    Returns:
        bool: Whether the given archive member is safe to extract.

    """
    # PurePath is the parent class of the Path class
    # PurePath has no filesystem access, e.g. no reading or writing data is allowed
    windows_path = PureWindowsPath(member_name)

    normalized_name = member_name.replace("\\", "/")
    member_path = PurePosixPath(normalized_name)

    if (
        not member_name  # an empty archive name does not identify a usable member
        or "\x00" in member_name  # NULs can be handled inconsistently by path APIs
        or member_path.is_absolute()  # reject POSIX-rooted paths
        or windows_path.is_absolute()  # reject Windows-rooted paths on any host
        or windows_path.drive  # reject drive-qualified paths, including drive-relative ones
        or ".." in member_path.parts  # reject parent traversal components
    ):
        return False

    # resolve first so this also rejects paths that escape through symlinks
    resolved_destination = destination.resolve()
    candidate = (resolved_destination / Path(*member_path.parts)).resolve()

    return candidate.is_relative_to(resolved_destination)


def atomic_write(target_file_path: Path, file_content: str, encoding: str = "utf-8") -> None:
    """Safely writes content to a file using a temporary file in the same directory.

    This prevents partial or corrupted writes if the process is interrupted.

    Args:
        target_file_path (Path): Target file path.
        file_content (str): Text content to write to the target file.
        encoding (str, optional): Which encoding to use for the text content. Defaults to "utf-8".

    """
    target_file_path.parent.mkdir(parents=True, exist_ok=True)
    temp_file_path = None

    try:
        with NamedTemporaryFile(mode="w", dir=target_file_path.parent, delete=False, encoding=encoding) as ntf:
            temp_file_path = Path(ntf.name)

            print(ntf)
            print(ntf.name)
            print(ntf.fileno())

            ntf.write(file_content)
            ntf.flush()  # send data from Python memory to OS
            os.fsync(ntf.fileno())

        temp_file_path.replace(target_file_path)
    finally:
        if temp_file_path and temp_file_path.exists():
            with contextlib.suppress(OSError):
                temp_file_path.unlink()


def example_1_basics() -> None:
    print(Path.cwd())
    print(Path.home())

    base_path = Path("filesndirstmp")  # relative to cwd

    tmp_dir = base_path / Path("tmp")

    tmp_archive_path = tmp_dir / "tmp.tar.gz"

    print(tmp_archive_path)
    print(tmp_archive_path.resolve())
    print(tmp_archive_path.name)
    print(tmp_archive_path.stem)
    print(tmp_archive_path.suffix)
    print(tmp_archive_path.suffixes)
    print(tmp_archive_path.parent)
    for parent in tmp_archive_path.parents:
        print(parent)
    print(tmp_archive_path.parts)
    print(tmp_archive_path.resolve().anchor)
    print(tmp_archive_path.with_suffix(".zip"))
    print(tmp_archive_path.with_name(f"{tmp_archive_path.name.removesuffix('.tar.gz')}.zip"))

    log_file_path = Path("loggingdates.log")

    with log_file_path.open("r", encoding="utf-8") as file:
        # yield lines one by one
        for line in file:
            print(line.rstrip())

    # read all lines into memory
    lines = log_file_path.read_text(encoding="utf-8")
    print(lines)

    tmp_log_path = tmp_dir / "tmp.log"
    tmp_log_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_log_path.write_text("Initial log\n", encoding="utf-8")
    with tmp_log_path.open("a", encoding="utf-8") as file:
        file.write("Nexttt log\n")
    print(tmp_log_path.read_text(encoding="utf-8"))

    shutil.copy2(tmp_log_path, Path("filesndirstmp.log"))
    shutil.rmtree(base_path)


def example_2_finding_filesndirs() -> None:
    for entry in sorted(Path().iterdir()):
        if entry.is_file():
            print(f"(FILE): {entry}")
        elif entry.is_dir():
            print(f"(DCTR): {entry}")

    # think of glob patterns as a friendly, lightweight shorthand specifically tailored for finding files,
    # whereas regular expressions are a heavy-duty language for searching and manipulating text
    # for example, if you want to match a file named "report_2026.csv"
    # - glob: report_*.csv
    # - regex: ^report_.*\.csv$

    for entry in sorted(Path().glob("*.py")):
        print(entry)

    for pattern in ("*.yml", "*.yaml"):
        for entry in Path().glob(pattern):
            print(entry)

    # KB, MB, GB, TB - decimal units (multiplier is 1000)
    # KiB, MiB, GiB, TiB - binary units (multiplier is 1024)
    # for example, 1KB = 1000 bytes, 1KiB = 1024 bytes, 1MB = 1000*1000 bytes, 1MiB = 1024*1024 bytes, etc.

    big_thres = 5000
    for entry in Path("src").rglob("*.py"):
        is_big = entry.stat().st_size > big_thres
        print(f"(BIG) {entry}" if is_big and entry.exists() else f"      {entry}")

    print()
    for root, dirs, filenames in Path("src").walk():
        print(root)
        print(dirs)
        print(filenames)
        for filename in filenames:
            print(root / filename)
        print()


def example_3_csv() -> None:
    field_names = FieldNamesCSV(f1="i", f2="s")
    new_csv_data: list[DataCSV] = [
        DataCSV(i=random.randint(-10, 10), s=string.ascii_letters[random.randint(0, len(string.ascii_letters) - 1)])
        for _ in range(2)
    ]

    csv_path = Path("filesndirstmp.csv")

    with csv_path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(field_names))
        if (not csv_path.exists()) or (csv_path.stat().st_size <= 0):
            writer.writeheader()
        writer.writerows([data.model_dump() for data in new_csv_data])

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data = DataCSV.model_validate(row)
            print(data.i, data.s)


def example_4_download() -> None:
    tmp_img = Path("filesndirstmp.svg")

    if not tmp_img.exists():
        with requests.get(
            "https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            stream=True,
            timeout=10,
        ) as response:
            response.raise_for_status()

            # stream=True avoids downloading all (potentially very big) data contents into RAM
            # we get them on the fly in chunks

            with tmp_img.open("wb") as img:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        img.write(chunk)

    print(tmp_img.read_bytes())


def example_5_pickle() -> None:
    obj_to_pickle = FieldNamesCSV(f1="i", f2="s")
    pickled_data = pickle.dumps(obj_to_pickle)
    print(pickled_data)
    print(type(pickle.loads(pickled_data)))  # dangerous because allows execution of arbitrary code upon unpickling


def example_6_archives() -> None:
    shutil.make_archive("filesndirstmp", "zip", Path("tests"))

    with zipfile.ZipFile(Path("filesndirstmp.zip"), "r") as zf:
        print(zf.namelist())
        print()
        content = zf.read("expense_tracker/unit/test_expense.py")
        print(content)
        print()
        for info in zf.infolist():
            print(f"name: {info.filename}, size: {info.file_size}")
    print()

    safe_workdir = Path("extracted_dir")
    is_safe = True

    with zipfile.ZipFile(Path("filesndirstmp.zip"), "r") as zf:
        for info in zf.infolist():
            if not is_safe_archive_member(info.filename, safe_workdir):
                print(f"Unsafe archive member: {info.filename!r}")
                is_safe = False
            else:
                print("Safe member!!!")
    print()

    if is_safe:
        # unpacking can be dangerous
        # malicious archives can contain paths that "escape" the target directory, e.g. ../../etc/passwd
        # validate member paths before extraction, but still use a safe extraction method
        shutil.unpack_archive("filesndirstmp.zip", safe_workdir)
        print("Successfully unpacked!")


def example_7_tmp() -> None:
    atomic_write(Path("filesndirstmp.txt"), "Text contenttt\n")

    with TemporaryDirectory() as tmpdir:
        print(f"tmp_dir: {tmpdir}")
        workdir = Path(tmpdir)
        print(f"workdir: {workdir}")
        output = workdir / "output.txt"
        output.write_text("Output\n", encoding="utf-8")
        print(output.read_text(encoding="utf-8"))


def example_8_stats() -> None:
    print(dt.datetime.fromtimestamp(Path("webapp").stat().st_mtime, tz=dt.UTC))

    noxfile = Path("noxfile.py")
    stats = noxfile.stat()
    print(stats)

    if stat.S_ISDIR(stats.st_mode):
        print("It's a dir")
    elif stat.S_ISREG(stats.st_mode):
        print("It's a regular file")
    else:
        print("I dunno what is it")

    if stat.S_IRUSR & stats.st_mode:
        print("User can read")
    if stat.S_IWUSR & stats.st_mode:
        print("User can write")
    if stat.S_IXUSR & stats.st_mode:
        print("User can execute")

    print(oct(stat.S_IMODE(stats.st_mode)))

    Path.chmod(noxfile, stats.st_mode | stat.S_IXUSR)  # doesn't work on Windows
    stats = noxfile.stat()
    if stat.S_IRUSR & stats.st_mode:
        print("User can read")
    if stat.S_IWUSR & stats.st_mode:
        print("User can write")
    if stat.S_IXUSR & stats.st_mode:
        print("User can execute")


def example_9_os() -> None:
    noxfile = Path("noxfile.py")

    if os.access(noxfile, os.R_OK):
        print("File readable by the current user")
    if os.access(noxfile, os.W_OK):
        print("File writeable by the current user")
    if os.access(noxfile, os.X_OK):
        print("File executeable by the current user")

    print(os.name)
    print(os.environ["LANG"])
    print(os.getenv("LANG"))

    # app crashes with os.environ[""] when a required env var is missing, os.getenv would return None instead
    load_dotenv(".env.example")
    print(os.environ["SECRET_KEY"])


def main() -> None:
    # note: handling file exceptions will be skipped here, for simplicity
    # tip: in practice, you should use dry runs before some dangerous file operations

    # print("Example 1 (basics):")
    # example_1_basics()
    # print()

    # print("Example 2 (finding files and dirs):")
    # example_2_finding_filesndirs()
    # print()

    # print("Example 3 (csv):")
    # example_3_csv()
    # print()

    # print("Example 4 (downloading a file):")
    # example_4_download()
    # print()

    # print("Example 5 (pickling & unpickling):")
    # example_5_pickle()
    # print()

    # print("Example 6 (archives):")
    # example_6_archives()
    # print()

    # print("Example 7 (tmp):")
    # example_7_tmp()
    # print()

    # print("Example 8 (stats):")
    # example_8_stats()
    # print()

    print("Example 9 (os)")
    example_9_os()
    print()


if __name__ == "__main__":
    main()
