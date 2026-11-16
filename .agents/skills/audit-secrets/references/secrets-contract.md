# Secrets standard

SOPS + age is the source of truth. This file is the only copy. A project cites it from `AGENTS.md` and states only its own section names and store paths.

The loopback starter password stays in Compose. It is not a secret and it is not an entry in the store. A real credential, including one used on a laptop, goes in the local encrypted store.

| Id | Rule |
|----|------|
| S1 | The store is SOPS + age. A plaintext `.env`, an image layer, and a Kubernetes Secret are not the source of truth. |
| S2 | A schema in code names every section and every variable. An unknown section or key is an error. A process receives only the names its section declares. Empty values are not forwarded. A non-empty shell variable of a declared name wins for that run. Shared credentials live in one section, and only a consumer that declares them receives them. |
| S3 | Decryption happens in the process that starts the command. Values exist in that process's environment and nowhere else. Nothing decrypted is written to disk, a `.env` file, an image `ENV`, or a name that starts with `NEXT_PUBLIC_`. The child is started with `PYTHON_DOTENV_DISABLED=1`. `.env.example` lists non-secret settings only. |
| S4 | The local store and the production store are different files with different recipients. A developer key cannot decrypt production. Production has three age recipients: the host key file at mode `0400` that stays on the host, a maintainer, and an offline backup kept outside every repository. CI does not hold an age private key. |
| S5 | `APP_ENV` is unset or `production`. Unset refuses a database host other than loopback. `production` refuses to start when `sops`, the age key, or the store is missing, when a required name is absent, when `DATABASE_URL` uses the starter password, or when the database connection is not `sslmode=verify-full`. Logs and errors include neither a secret nor a full connection URL. A running process reads a rotation at its next start. |
| S6 | An agent does not read the age key, decrypt the store, or print a secret value. It does not run the export helper in front of a command that can print its environment. `AGENTS.md` states this. A data lookup an agent needs uses a read-only role and masks store values. Tool permission files stay per tool. |
| S7 | `make check` fails when a committed `*.enc.yaml` holds a plaintext value or when an age private key is in the tree. `.env` is gitignored. Decrypted env files and age private keys are gitignored. |
| S8 | Fewer than two recipients is a warning on the local store. Production requires three. Changing recipients is `sops updatekeys`. After a key is removed or lost, rotate the values as well. The old ciphertext stays in git history. |

## Evidence

S1 and S3: `.sops.yaml`, the store paths, and the export helper. S2: the schema. S4: the creation rules and, when a production store exists, the recipient lines in its metadata. Those lines are plaintext. Do not decrypt. S5: the `APP_ENV` branch that builds `DATABASE_URL`. S6: `AGENTS.md`. S7: run `make check`. S8: the recipient check, without printing values.

Cloud secret managers, KMS, and workload identity are outside this version.
