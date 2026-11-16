"""The one reader of the SOPS + age stores.

secrets/local.enc.yaml is the local store. secrets/production.enc.yaml is production.
They have different recipients. A section or key that is not declared is an error.
Decrypted values stay in memory and in a child's environment. This module never
writes them to disk.

Add a shared credential by naming it in SCHEMA["providers"] and in CONSUMES for
each process that may receive it. A process receives only those names plus its
own section.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from collections.abc import Mapping
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCAL_STORE = ROOT / "secrets" / "local.enc.yaml"
PRODUCTION_STORE = ROOT / "secrets" / "production.enc.yaml"
DEFAULT_AGE_KEY_FILE = Path.home() / ".config" / "sops" / "age" / "keys.txt"

OWN: dict[str, frozenset[str]] = {
    "app": frozenset({"DATABASE_URL"}),
}
CONSUMES: dict[str, frozenset[str]] = {
    "app": frozenset(),
}
SCHEMA: dict[str, frozenset[str]] = {"providers": frozenset(), **OWN}
SECTIONS = tuple(OWN)


class SecretsError(RuntimeError):
    """The encrypted store could not be read or does not match SCHEMA."""


def parse(document: str) -> dict[str, dict[str, str]]:
    """Validate decrypted JSON against SCHEMA. Return {section: {ENV_NAME: value}}."""
    try:
        raw = json.loads(document)
    except json.JSONDecodeError as error:
        raise SecretsError(f"Decrypted secrets are not valid JSON: {error}") from error
    if not isinstance(raw, dict):
        raise SecretsError("Decrypted secrets must be a mapping of sections.")
    parsed: dict[str, dict[str, str]] = {}
    for section, entries in raw.items():
        if section == "sops":
            continue
        if section not in SCHEMA:
            raise SecretsError(f"Unknown secrets section {section!r}; expected {sorted(SCHEMA)}.")
        if not isinstance(entries, dict):
            raise SecretsError(f"Secrets section {section!r} must be a mapping.")
        values: dict[str, str] = {}
        for key, value in entries.items():
            name = str(key).upper()
            if name not in SCHEMA[section]:
                raise SecretsError(f"Unknown key {key!r} in secrets section {section!r}.")
            if value is None or value == "":
                continue
            if isinstance(value, (dict, list)):
                raise SecretsError(f"{section}.{key} must be a scalar string.")
            values[name] = str(value)
        parsed[section] = values
    return parsed


def required_recipients(path: Path) -> int:
    """Production needs the host, a maintainer, and an offline backup."""
    if "production" in path.name:
        return 3
    return 2


def recipient_count(path: Path) -> int:
    """Age recipients that can decrypt the store, from its plaintext sops metadata."""
    if not path.is_file():
        raise SecretsError(f"{path} is missing. Create it with sops. See secrets/README.md.")
    return len(re.findall(r"\brecipient:\s*age1", path.read_text(encoding="utf-8")))


def decrypt(path: Path = LOCAL_STORE) -> dict[str, dict[str, str]]:
    """Decrypt with sops. A missing file, binary, or key is an error."""
    if not path.is_file():
        raise SecretsError(f"{path} is missing. Create it with sops. See secrets/README.md.")
    sops = shutil.which("sops")
    if sops is None:
        raise SecretsError("sops is not on PATH (brew install sops age).")
    env = dict(os.environ)
    if not env.get("SOPS_AGE_KEY_FILE") and not env.get("SOPS_AGE_KEY"):
        if not DEFAULT_AGE_KEY_FILE.is_file():
            raise SecretsError(
                "No age key: set SOPS_AGE_KEY_FILE or create "
                f"{DEFAULT_AGE_KEY_FILE} (age-keygen -o ...)."
            )
        env["SOPS_AGE_KEY_FILE"] = str(DEFAULT_AGE_KEY_FILE)
    result = subprocess.run(
        [sops, "decrypt", "--output-type", "json", str(path)],
        capture_output=True,
        text=True,
        check=False,
        env=env,
        timeout=30,
    )
    if result.returncode != 0:
        detail = result.stderr.strip()
        raise SecretsError(
            f"sops could not decrypt {path.name} (is the public key in .sops.yaml and "
            f"the file re-keyed?): {detail}"
        )
    return parse(result.stdout)


def settings_for(
    section: str,
    store: Mapping[str, Mapping[str, str]],
    environ: Mapping[str, str] | None = None,
) -> dict[str, str]:
    """Environment for one process: its section, the shared names it declares, then the shell.

    Only declared names are forwarded. A non-empty shell variable of the same name wins.
    """
    if section not in SECTIONS:
        raise SecretsError(f"Unknown secrets section {section!r}; expected {list(SECTIONS)}.")
    values = {key: value for key, value in store.get(section, {}).items() if key in OWN[section]}
    shared = CONSUMES[section]
    values.update(
        {key: value for key, value in store.get("providers", {}).items() if key in shared}
    )
    shell = os.environ if environ is None else environ
    for name in OWN[section] | shared:
        if shell.get(name):
            values[name] = shell[name]
    return values
