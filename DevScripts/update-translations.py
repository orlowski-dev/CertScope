#!/usr/bin/env python3

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT / "CertScope"
PO_DIR = PROJECT / "po"
OUTPUT = PO_DIR / "messages.pot"

EXCLUDED_DIRS = {"bin", "obj", ".git"}


def run(*args: str) -> None:
    subprocess.run(
        args,
        cwd=ROOT,
        check=True,
    )


def find_sources(extension: str) -> list[str]:
    return sorted(
        str(path.relative_to(ROOT))
        for path in PROJECT.rglob(f"*{extension}")
        if not any(
            part in EXCLUDED_DIRS
            for part in path.relative_to(PROJECT).parts
        )
    )


def extract_csharp(
    files: list[str],
    output: Path,
) -> None:
    if not files:
        return

    print("Extracting C# translations...")

    run(
        "xgettext",
        "--language=C#",
        "--from-code=UTF-8",
        "--add-comments=Translators:",
        "--force-po",
        "--keyword",
        "--keyword=Gettext.Get:1",
        "--keyword=Gettext.GetPlural:1,2",
        "--output", str(output),
        *files,
    )


def extract_blueprint(
    files: list[str],
    output: Path,
    join_existing: bool,
) -> None:
    if not files:
        return

    print("Extracting Blueprint translations...")

    arguments = [
        "xgettext",
        "--language=C",
        "--from-code=UTF-8",
        "--add-comments=Translators:",
        "--force-po",
        "--keyword",
        "--keyword=_:1",
        "--keyword=C_:1c,2",
        "--output", str(output),
    ]

    if join_existing:
        arguments.append("--join-existing")

    arguments.extend(files)

    run(*arguments)


def update_template(
    csharp_files: list[str],
    blueprint_files: list[str],
) -> None:
    PO_DIR.mkdir(parents=True, exist_ok=True)

    # Temporary file on the same filesystem as messages.pot
    fd, temporary_name = tempfile.mkstemp(
        prefix=".messages.",
        suffix=".pot",
        dir=PO_DIR,
    )

    os.close(fd)
    temporary_path = Path(temporary_name)

    # xgettext --join-existing requires an existing valid catalog.
    # Delete the empty file before extraction.
    temporary_path.unlink()

    try:
        if csharp_files:
            extract_csharp(csharp_files, temporary_path)

        if blueprint_files:
            extract_blueprint(
                blueprint_files,
                temporary_path,
                join_existing=temporary_path.exists(),
            )

        # Ensure extraction generated a valid file
        if not temporary_path.is_file():
            raise RuntimeError(
                "Translation template was not generated."
            )

        # Validate generated POT before replacing the existing one
        run(
            "msgfmt",
            "--check",
            "-o", os.devnull,
            str(temporary_path),
        )

        # Atomic replacement
        os.replace(temporary_path, OUTPUT)

    finally:
        temporary_path.unlink(missing_ok=True)


def main() -> int:
    csharp_files = find_sources(".cs")
    blueprint_files = find_sources(".blp")

    print(f"C# files: {len(csharp_files)}")
    print(f"Blueprint files: {len(blueprint_files)}")

    if not csharp_files and not blueprint_files:
        print("No source files found.", file=sys.stderr)
        return 1

    try:
        update_template(csharp_files, blueprint_files)

        print(f"Updated: {OUTPUT.relative_to(ROOT)}")
        return 0

    except FileNotFoundError as error:
        print(
            f"Required executable or file not found: {error.filename}",
            file=sys.stderr,
        )
        return 1

    except subprocess.CalledProcessError as error:
        print(
            f"Command failed (exit code {error.returncode}): "
            f"{error.cmd}",
            file=sys.stderr,
        )
        return 1

    except (OSError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
