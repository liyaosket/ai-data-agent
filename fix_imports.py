from pathlib import Path
import re
import shutil
from datetime import datetime


# 项目内部模块列表
INTERNAL_MODULES = {
    "execution_trace",
    "task_agent",
    "llm_cost",
    "cached_llm",
    "metrics",
    "metrics_store",
    "metrics_registry",
    "task_runner",
    "context_manager",
    "retry_policy",
    "task_record",
    "tools",
    "llm_cache",
    "memory_cache_backend",
    "cache_backend",
    "query",
    "db",
    "sql_validator",
    "result_store",
    "schema",
    "response_serializer",
}


APP_DIR = Path("app")


BACKUP_DIR = Path(
    ".import_backup_"
    + datetime.now().strftime("%Y%m%d_%H%M%S")
)


def backup(file):

    backup_file = (
        BACKUP_DIR / file
    )

    backup_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(
        file,
        backup_file,
    )


def fix_file(file):

    text = file.read_text(
        encoding="utf-8"
    )

    original = text


    # from xxx import xxx
    pattern = (
        r"^from "
        r"(?!app\.)"
        r"([a-zA-Z_][\w]*)"
        r"(\.[a-zA-Z_][\w]*)*"
        r" import "
    )


    def replace_from(match):

        module = match.group(1)

        if module in INTERNAL_MODULES:

            rest = (
                match.group(2)
                or ""
            )

            return (
                f"from app."
                f"{module}"
                f"{rest}"
                f" import "
            )

        return match.group(0)


    text = re.sub(
        pattern,
        replace_from,
        text,
        flags=re.MULTILINE,
    )


    if text != original:

        backup(file)

        file.write_text(
            text,
            encoding="utf-8",
        )

        print(
            f"[UPDATED] {file}"
        )


def main():

    if not APP_DIR.exists():

        print(
            "app directory not found"
        )

        return


    for file in APP_DIR.rglob(
        "*.py"
    ):

        fix_file(file)


    print()
    print(
        "Import cleanup finished."
    )

    if BACKUP_DIR.exists():

        print(
            "Backup:",
            BACKUP_DIR,
        )


if __name__ == "__main__":
    main()
