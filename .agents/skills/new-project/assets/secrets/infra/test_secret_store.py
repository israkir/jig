"""Guards for the store schema and the offline ciphertext check."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_store
import secret_store


class SchemaTests(unittest.TestCase):
    def test_unknown_key_is_rejected(self) -> None:
        """Guards: an unknown key in the store is kept."""
        with self.assertRaises(secret_store.SecretsError):
            secret_store.parse('{"app": {"other_secret": "x"}}')

    def test_unknown_section_is_rejected(self) -> None:
        """Guards: an unknown section in the store is kept."""
        with self.assertRaises(secret_store.SecretsError):
            secret_store.parse('{"billing": {"token": "x"}}')

    def test_empty_value_is_dropped(self) -> None:
        """Guards: an empty secret is forwarded to the process."""
        parsed = secret_store.parse('{"app": {"database_url": ""}}')
        self.assertEqual(parsed["app"], {})

    def test_only_declared_names_are_forwarded(self) -> None:
        """Guards: a shared credential reaches a process that does not declare it."""
        store = {
            "providers": {"FRED_API_KEY": "x"},
            "app": {"DATABASE_URL": "postgresql://example", "OTHER": "no"},
        }
        self.assertEqual(
            secret_store.settings_for("app", store, {}),
            {"DATABASE_URL": "postgresql://example"},
        )

    def test_shell_override_wins_and_an_empty_shell_value_does_not(self) -> None:
        """Guards: an empty shell variable wipes the stored database URL."""
        store = {"app": {"DATABASE_URL": "postgresql://stored"}}
        self.assertEqual(
            secret_store.settings_for("app", store, {"DATABASE_URL": "postgresql://shell"}),
            {"DATABASE_URL": "postgresql://shell"},
        )
        self.assertEqual(
            secret_store.settings_for("app", store, {"DATABASE_URL": ""}),
            {"DATABASE_URL": "postgresql://stored"},
        )


class ScanTests(unittest.TestCase):
    def test_plaintext_store_is_detected(self) -> None:
        """Guards: a plaintext value in a committed enc file is accepted."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = root / "secrets"
            store.mkdir()
            (store / "local.enc.yaml").write_text(
                "app:\n    database_url: hunter2\nsops:\n    version: 3\n",
                encoding="utf-8",
            )
            failures = check_store.scan(root)
        self.assertTrue(any("database_url" in failure for failure in failures))

    def test_encrypted_store_passes(self) -> None:
        """Guards: SOPS ciphertext is reported as plaintext."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "local.enc.yaml").write_text(
                "app:\n    database_url: ENC[AES256_GCM,data:abc]\nsops:\n    version: 3\n",
                encoding="utf-8",
            )
            self.assertEqual(check_store.scan(root), [])

    def test_private_key_is_detected(self) -> None:
        """Guards: an age private key in the tree is accepted."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            note = root / "notes.txt"
            note.write_text("token " + check_store.PRIVATE_KEY + "QQ\n", encoding="utf-8")
            failures = check_store.scan(root)
        self.assertTrue(any("age private key" in failure for failure in failures))


class RecipientTests(unittest.TestCase):
    def test_recipient_count_reads_plaintext_metadata(self) -> None:
        """Guards: a second age recipient is not counted."""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "local.enc.yaml"
            path.write_text(
                "sops:\n    recipient: age1aaa\n    recipient: age1bbb\n",
                encoding="utf-8",
            )
            self.assertEqual(secret_store.recipient_count(path), 2)
        self.assertEqual(secret_store.required_recipients(Path("local.enc.yaml")), 2)
        self.assertEqual(secret_store.required_recipients(Path("production.enc.yaml")), 3)


if __name__ == "__main__":
    unittest.main()
