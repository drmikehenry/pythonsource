#!/usr/bin/env python3

import hashlib
from pathlib import Path
import re
import typing as T

import httpx

VersionTuple = T.Tuple[int, ...]

local_root_path = Path("python")
base_url = "https://www.python.org/ftp/python"


def parse_version_tuple(s: str) -> VersionTuple:
    return tuple(int(v) for v in s.split("."))


def version_tuple_str(v: VersionTuple) -> str:
    return ".".join(str(i) for i in v)


def version_tuple_widen(vt: VersionTuple) -> VersionTuple:
    while len(vt) < 3:
        vt = vt + (0,)
    return vt


def next_minor_version(vstr: str) -> str:
    vt = parse_version_tuple(vstr)
    vt2 = vt[0], (vt[1] + 1), 0
    return version_tuple_str(vt2)


def version_less(v1: str, v2: str) -> bool:
    vt1 = version_tuple_widen(parse_version_tuple(v1))
    vt2 = version_tuple_widen(parse_version_tuple(v2))
    return vt1 < vt2


def version_less_equal(v1: str, v2: str) -> bool:
    vt1 = version_tuple_widen(parse_version_tuple(v1))
    vt2 = version_tuple_widen(parse_version_tuple(v2))
    return vt1 <= vt2


min_versions = """
2.7.15
3.5.7
3.6.8
3.7.2
3.8.0
3.9.0
3.10.0
""".split()


def want_version(version: str) -> bool:
    for min_ver in min_versions:
        next_ver = next_minor_version(min_ver)
        if version_less_equal(min_ver, version) and version_less(
            version, next_ver
        ):
            return True
    return False


# Note: only .tgz and .tar.xz needed.

# "3.6.7" -> "Python-3.6.7.tar.xz"
Artifacts = T.Dict[str, str]

# "Python-3.6.7.tar.xz" -> sha256 hexdigest.
Hashes = T.Dict[str, str]


def pyenv_scan(path: Path) -> T.Tuple[Artifacts, Hashes]:
    artifacts = dict()
    hashes = dict()
    rex = re.compile(
        r"""
        www.python.org/ftp/python/
            (?P<version>\d+(?:\.\d+)+)
            /(?P<name>[^#/]+?)
            [#]
            (?P<hash_str>\w{64})\b
        """,
        re.VERBOSE,
    )
    for f in path.glob("plugins/python-build/share/python-build/*"):
        if not f.is_file or not re.search(r"^\d+(?:\.\d+)+$", f.name):
            continue
        text = f.read_text()
        for m in rex.finditer(text):
            version = m.group("version")
            name = m.group("name")
            hash_str = m.group("hash_str")
            if version not in artifacts or artifacts[version].endswith(".tgz"):
                artifacts[version] = name
                hashes[name] = hash_str
    sorted_artifacts = {
        k: artifacts[k] for k in sorted(artifacts, key=parse_version_tuple)
    }
    return sorted_artifacts, hashes


def path_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_matches(path: Path, hash_str: str) -> bool:
    if path.is_file():
        return hash_str == path_hash(path)
    return False


def download_one(path: Path, url: str, hash_str: str) -> bool:
    if path.is_file():
        if hash_matches(path, hash_str):
            print(f"[cached] {path}")
            return True
        print(f"[unlink] {path}")
        path.unlink()

    print(f"[download] {path}")
    r = httpx.get(url)
    with path.open("wb") as f:
        f.write(r.content)

    if not path.is_file():
        print(f"[failed] {path}")
        return False
    if not hash_matches(path, hash_str):
        print(f"[bad hash] {path}")
        return False
    return True


def download_all(artifacts: Artifacts, hashes: Hashes) -> None:
    total = 0
    bad = 0
    for ver, name in artifacts.items():
        if want_version(ver):
            total += 1
            rel_path = f"{ver}/{name}"
            local_path = local_root_path / rel_path
            local_path.parent.mkdir(parents=True, exist_ok=True)
            url = f"{base_url}/{rel_path}"
            hash_str = hashes[name]
            if not download_one(local_path, url, hash_str):
                bad += 1
    print(f"Total versions: {total}")
    if bad > 0:
        print(f"*** {bad} bad versions")


def main():
    artifacts, hashes = pyenv_scan(Path("pyenv"))
    download_all(artifacts, hashes)


if __name__ == "__main__":
    main()
