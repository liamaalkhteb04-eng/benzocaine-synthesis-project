from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path

EXCLUDED_NAMES = {"PACKAGE-MANIFEST.json", "PACKAGE-MANIFEST.sha256"}
EXCLUDED_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
MODEL_WEIGHT_SUFFIXES = {".pt", ".pth", ".bin", ".onnx", ".safetensors", ".ckpt", ".h5", ".pb"}
MAX_PACKAGE_FILE_BYTES = 50 * 1024 * 1024

def is_git_root(root: Path) -> bool:
    try:
        top = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
        ).decode("utf-8").strip()
        return Path(top).resolve() == root.resolve()
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
        return False

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def canonical_content(path: Path, relative_path: str, text_attributes: dict[str, str]) -> bytes:
    """Return bytes as stored by Git, so hashes survive checkout EOL conversion."""
    data = path.read_bytes()
    attribute = text_attributes.get(relative_path, "unspecified")
    if attribute == "unset":
        return data
    if attribute == "set" or (attribute in {"auto", "unspecified"} and b"\x00" not in data[:8000]):
        return data.replace(b"\r\n", b"\n")
    return data

def git_text_attributes(root: Path, relative_paths: list[str]) -> dict[str, str]:
    """Read .gitattributes in one batch; use a text heuristic outside a Git checkout."""
    if not relative_paths or not is_git_root(root):
        return {}
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "check-attr", "-z", "--stdin", "text"],
            input=("\0".join(relative_paths) + "\0").encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return {}
    fields = result.stdout.split(b"\0")
    attributes = {}
    for index in range(0, len(fields) - 2, 3):
        rel, name, value = (field.decode("utf-8") for field in fields[index:index + 3])
        if name == "text":
            attributes[rel] = value
    return attributes

def git_index_contents(root: Path, relative_paths: list[str]) -> dict[str, bytes]:
    """Read committed/staged blobs so untouched legacy CRLF blobs keep their exact hash."""
    if not relative_paths or not is_git_root(root):
        return {}
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "cat-file", "--batch"],
            input=("".join(f":{rel}\n" for rel in relative_paths)).encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return {}
    content = {}
    offset = 0
    try:
        for rel in relative_paths:
            end = result.stdout.index(b"\n", offset)
            _, object_type, raw_size = result.stdout[offset:end].decode("ascii").split()
            offset = end + 1
            size = int(raw_size)
            blob = result.stdout[offset:offset + size]
            if object_type != "blob" or len(blob) != size or result.stdout[offset + size:offset + size + 1] != b"\n":
                return {}
            content[rel] = blob
            offset += size + 1
    except (ValueError, UnicodeDecodeError):
        return {}
    return content

def git_worktree_changes(root: Path) -> tuple[set[str], set[str]]:
    """Return unstaged tracked changes and unstaged untracked files."""
    if not is_git_root(root):
        return set(), set()
    try:
        modified = subprocess.check_output(
            ["git", "-C", str(root), "diff", "--name-only", "-z"], stderr=subprocess.DEVNULL
        ).decode("utf-8").split("\0")
        untracked = subprocess.check_output(
            ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard", "-z"], stderr=subprocess.DEVNULL
        ).decode("utf-8").split("\0")
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
        return set(), set()
    return {x for x in modified if x}, {x for x in untracked if x}

def main() -> int:
    ap = argparse.ArgumentParser(description="Build a relative-path SHA-256 manifest for the public project package.")
    ap.add_argument("package", type=Path)
    args = ap.parse_args()
    root = args.package.resolve()
    candidates = sorted(
        p for p in root.rglob("*")
        if p.is_file()
        and not any(part in EXCLUDED_DIRS for part in p.relative_to(root).parts)
        and p.name not in EXCLUDED_NAMES
        and p.suffix.lower() not in EXCLUDED_SUFFIXES
    )
    relative_paths = [p.relative_to(root).as_posix() for p in candidates]
    text_attributes = git_text_attributes(root, relative_paths)
    index_contents = git_index_contents(root, relative_paths)
    unstaged_modified, unstaged_untracked = git_worktree_changes(root)
    entries = []
    for p in candidates:
        rel = p.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in rel.parts) or p.name in EXCLUDED_NAMES or p.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        if p.name == ".env" or p.name.lower().endswith(".key"):
            raise SystemExit(f"refusing to include sensitive filename: {rel.as_posix()}")
        if p.suffix.lower() in MODEL_WEIGHT_SUFFIXES:
            raise SystemExit(f"refusing to include model weight asset: {rel.as_posix()}")
        if p.stat().st_size > MAX_PACKAGE_FILE_BYTES:
            raise SystemExit(f"refusing to include oversized file (>50 MiB): {rel.as_posix()}")
        relative = rel.as_posix()
        if relative in index_contents and relative not in unstaged_modified and relative not in unstaged_untracked:
            canonical = index_contents[relative]
        else:
            canonical = canonical_content(p, relative, text_attributes)
        entries.append({"path": rel.as_posix(), "size_bytes": len(canonical), "sha256": hashlib.sha256(canonical).hexdigest()})
    manifest = {"format": "professor-package-manifest-v1", "file_count": len(entries), "files": entries}
    manifest_path = root / "PACKAGE-MANIFEST.json"
    with manifest_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    sidecar_path = root / "PACKAGE-MANIFEST.sha256"
    with sidecar_path.open("w", encoding="ascii", newline="\n") as f:
        f.write(f"{sha(manifest_path)}  PACKAGE-MANIFEST.json\n")
    print(f"wrote {manifest_path.name}: {len(entries)} files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
