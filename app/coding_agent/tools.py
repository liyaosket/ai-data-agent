from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def list_files(relative_path="."):
    """
    List files and directories inside the project.
    """
    target = (PROJECT_ROOT / relative_path).resolve()

    if not target.is_relative_to(PROJECT_ROOT):
        raise ValueError("Path escapes project root")

    if not target.exists():
        raise FileNotFoundError(relative_path)

    items = []

    for path in sorted(target.iterdir()):
        items.append({
            "name": path.name,
            "type": "directory" if path.is_dir() else "file",
        })

    return items


def read_file(relative_path):
    """
    Read a text file inside the project.
    """
    target = (PROJECT_ROOT / relative_path).resolve()

    if not target.is_relative_to(PROJECT_ROOT):
        raise ValueError("Path escapes project root")

    if not target.is_file():
        raise FileNotFoundError(relative_path)

    return target.read_text(encoding="utf-8")


def search_code(query, relative_path="."):
    """
    Search text recursively inside project files.
    """
    root = (PROJECT_ROOT / relative_path).resolve()

    if not root.is_relative_to(PROJECT_ROOT):
        raise ValueError("Path escapes project root")

    if not root.exists():
        raise FileNotFoundError(relative_path)

    results = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        # Skip common generated / dependency directories.
        if any(
            part in {
                ".git",
                ".venv",
                "__pycache__",
                "node_modules",
            }
            for part in path.parts
        ):
            continue

        try:
            text = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except Exception:
            continue

        for line_number, line in enumerate(
            text.splitlines(),
            start=1,
        ):
            if query.lower() in line.lower():
                results.append({
                    "file": str(path.relative_to(PROJECT_ROOT)),
                    "line": line_number,
                    "content": line.strip(),
                })

    return results


import subprocess


def run_command(command, timeout=30):
    """
    Execute a shell command inside the project root.
    """
    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
