# Spec: Resurrection Logic

## Goal
Create a dependency manager that aggressively updates `package.json`.

## Requirements
1.  **Lockfile Handling:** If `package-lock.json` exists, delete it. It causes conflicts in dead repos.
2.  **Install Strategy:**
    * Try `npm install <pkg>@latest`.
    * If it fails, retry with `--force` and `--legacy-peer-deps`.
3.  **Output:** Return a dictionary of {success: [], failed: []}.