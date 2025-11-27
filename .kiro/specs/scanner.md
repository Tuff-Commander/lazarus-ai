# Spec: Project Scanner

## Goal
Create a Python module that acts as the "Death Report" generator.

## Input
- A GitHub Repository URL (string).

## Process
1. **Clone:** Use GitPython to clone the repo to a temporary directory `temp_resurrection/[timestamp]`.
2. **Identify:** Check if `package.json` exists. If not, raise `InvalidProjectError`.
3. **Parse:** Read `dependencies` and `devDependencies`.
4. **Analyze:** - Fetch the latest version of each package from the NPM Registry API.
   - Calculate "Years Behind" (difference between current version date and installed version date).
5. **Security Check:** (Placeholder) Create a structure to hold vulnerability counts.

## Output
Return a Dictionary (JSON compatible) containing:
- Repository Metadata (Stars, Last Commit Date)
- Dependency Health (Total, Outdated Count)
- "Resurrection Score" (0-100, where 0 is dead and 100 is healthy).