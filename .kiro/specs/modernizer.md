# Spec: Code Modernizer

## Goal
A script that scans a folder for `.js` files and replaces legacy syntax.

## Patterns
1.  Replace `var` with `let`.
2.  Replace `console.log` with `console.info`.

## constraints
* Must be recursive (walk through subfolders).
* Must ignore `node_modules`.
* Must return a count of files changed.