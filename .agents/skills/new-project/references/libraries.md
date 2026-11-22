# Libraries

Every surface that declares libraries follows this file. The current surfaces are the Python API and the Next.js web app. A later language or framework adds a row to the table and uses the same steps.

The copied manifests are floors, and each manifest is a set that installs together. Raise every direct dependency to the newest stable release that still resolves with the others in that manifest and passes that surface's checks. Keep the floor form the manifest already uses. The package manager may install a newer release above the floor you write.

The language runtime and the database image stay at the versions in the README and `compose.yaml`. Those are platform requirements.

## Manifests

| Surface | Manifest | Newest stable release | Floor form |
|---------|----------|----------------------|------------|
| API, Python | `apps/api/pyproject.toml` | `https://pypi.org/pypi/<name>/json`, the `info.version` field. An extra uses the package name (`uvicorn[standard]` is `uvicorn`). | `name>=X.Y.Z`, extra included |
| Web, Next.js | `apps/web/package.json` | `npm view <name> version` | `"name": "^X.Y.Z"` |

A later surface adds a row: its manifest path, how to read the newest stable release, and the floor form that manifest already uses. Dependencies and dev dependencies are both direct dependencies. Raise one manifest at a time, so a conflict stays inside one package manager.

## Raise the floors

Do this after the files are copied and the tokens are replaced, and before Verify. On an existing repository, raise only the dependencies the new surface added. Leave a floor the repository already had.

1. For each manifest in the table that this project has, read the newest stable release of each direct dependency.
2. When that release is newer than the copied floor, write it in using that row's floor form. Keep a floor at or above the version you copied.
3. When the registry cannot be read, keep the copied floor and say so.
4. Verify is the resolution. A resolver conflict names a constraint. Lower only the packages it names, in that manifest, to the newest release that satisfies the constraint, still at or above the copied floor, and resolve again.
5. When a Verify command fails because of a release you just wrote, step that package back to the newest release of the previous major, or to the copied floor when that is newer. Run the command again. Keep the newest floor for which Verify passes.

Report the floors you wrote and any package you stepped back.

## Later dependencies

A library added after the scaffold uses the row for its manifest and the same steps. It resolves with the floors already in that manifest. Leave an existing floor unless the new library cannot resolve without raising it.
