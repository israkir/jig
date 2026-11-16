# Secrets

`local.enc.yaml` is the local store. `production.enc.yaml` is the production store. Create each with `sops`. The schema is `infra/secrets/secret_store.py`.

The loopback database password is not an entry in either store.
