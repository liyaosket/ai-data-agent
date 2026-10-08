from app.coding_agent.tools import (
    list_files,
    read_file,
    search_code,
    run_command,
)


def main():
    print("=" * 60)
    print("LIST FILES")
    print("=" * 60)

    files = list_files("app")

    for item in files:
        print(item)

    print()
    print("=" * 60)
    print("READ FILE")
    print("=" * 60)

    content = read_file("app/query.py")

    print(content[:1000])

    print()
    print("=" * 60)
    print("SEARCH CODE")
    print("=" * 60)

    results = search_code("execute_query")

    for result in results[:20]:
        print(result)

    print()
    print("=" * 60)
    print("RUN COMMAND")
    print("=" * 60)

    result = run_command(
        "python -m pytest --collect-only -q"
    )

    print("returncode:", result["returncode"])
    print("stdout:")
    print(result["stdout"][:3000])
    print("stderr:")
    print(result["stderr"][:3000])


if __name__ == "__main__":
    main()
