"""Run a command with one section's decrypted settings. Nothing is written to disk.

    python3 infra/secrets/export_env.py app -- <command>
    python3 infra/secrets/export_env.py app --names
    python3 infra/secrets/export_env.py --store secrets/production.enc.yaml app -- <command>
    python3 infra/secrets/export_env.py --recipients

The child receives the section's settings and PYTHON_DOTENV_DISABLED=1. Values are
never printed. --names prints variable names only. Do not point this at a command
that prints its environment.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from secret_store import (
    LOCAL_STORE,
    PRODUCTION_STORE,
    SECTIONS,
    SecretsError,
    decrypt,
    recipient_count,
    required_recipients,
    settings_for,
)


def recipients_status(local: Path, production: Path) -> int:
    """0 when every present store has enough recipients, 3 for a local warning, 1 otherwise."""
    try:
        count = recipient_count(local)
    except SecretsError as error:
        sys.stderr.write(f"error: {error}\n")
        return 1
    status = 0
    if count < required_recipients(local):
        sys.stdout.write(
            f"{local.name}: {count} age recipient(s) - WARNING: fewer than two recipients; "
            "if they are lost the store is gone\n"
        )
        status = 3
    else:
        sys.stdout.write(f"{local.name}: {count} age recipient(s) - ok\n")
    if not production.is_file():
        return status
    try:
        prod_count = recipient_count(production)
    except SecretsError as error:
        sys.stderr.write(f"error: {error}\n")
        return 1
    needed = required_recipients(production)
    if prod_count < needed:
        sys.stdout.write(
            f"{production.name}: {prod_count} age recipient(s) - production requires {needed}\n"
        )
        return 1
    sys.stdout.write(f"{production.name}: {prod_count} age recipient(s) - ok\n")
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("section", nargs="?", choices=SECTIONS)
    parser.add_argument("--store", type=Path, default=LOCAL_STORE, help="encrypted store")
    parser.add_argument(
        "--recipients",
        action="store_true",
        help="check recipient counts without decrypting values",
    )
    parser.add_argument("--names", action="store_true", help="list variable names, no values")
    argv = sys.argv[1:]
    split = argv.index("--") if "--" in argv else len(argv)
    args = parser.parse_args(argv[:split])
    command = argv[split + 1 :]

    if args.recipients:
        return recipients_status(args.store.resolve(), PRODUCTION_STORE)
    if args.section is None:
        parser.error("a section is required")
    try:
        settings = settings_for(args.section, decrypt(args.store.resolve()))
    except SecretsError as error:
        sys.stderr.write(f"error: {error}\n")
        return 1
    if args.names:
        sys.stdout.write("".join(f"{name}\n" for name in sorted(settings)))
        return 0
    if not command:
        sys.stderr.write("error: give --names, or -- COMMAND to run.\n")
        return 2
    child = {**os.environ, **settings, "PYTHON_DOTENV_DISABLED": "1"}
    os.execvpe(command[0], command, child)
    return 1


if __name__ == "__main__":
    sys.exit(main())
