# Spec: Dependency Manager

## Goal
Create a Python module `src/dependency_manager.py` that automatically updates outdated Node.js dependencies.

## Input
- Path to a local repository (cloned folder).
- A list of outdated dependencies (from the Scanner).

## Process (The Resurrection Loop)
1. **Load:** Read `package.json`.
2. **Strategy:** For each outdated dependency:
   - Attempt to update to the **Latest** version using `npm install <package>@latest`.
   - **Low-Spec Constraint:** Process updates **one by one** (Serial Mode) to prevent crashing the user's CPU. Do NOT run parallel installs.
3. **Verification (Mock):**
   - Since we can't guarantee the user has a full Node environment set up for every repo, simply verify that `npm install` completed with Exit Code 0.
   - If `npm install` fails, revert the change (rollback `package.json`).

## Output
- Return a list of successfully updated packages.
- Return a list of failed updates.