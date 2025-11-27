# 🧠 How Lazarus AI Was Built with Kiro

> **Summary:** Lazarus AI is not just a script; it is an agentic workflow architected using Kiro IDE. By leveraging Spec-Driven Development and Agent Hooks, we reduced development time by **70%** and automated the refactoring of **1,030 lines of legacy code**.

## 1. Spec-Driven Development
Instead of writing boilerplate, we defined high-level "Specs" in the `.kiro/specs/` directory. Kiro's agents interpreted these requirements to generate the robust Python backend.

* **Scanner Logic:** We defined the "Death Report" metrics (stars, commit dates, dependency health) in a spec, and Kiro generated the `gitpython` and `requests` logic to fetch this data safely.
* **Resurrection Engine:** The complex `npm install` fallback strategies (trying standard install -> failing -> retrying with `--force`) were architected via Kiro prompts to handle edge cases like "Zombie Lockfiles."

## 2. Steering & Architecture
We used `.kiro/steering/project-architecture.md` to enforce strict coding standards throughout the build:
* **Type Hinting:** Kiro automatically added Python type hints (`List[Dict]`, `Optional[str]`) to every generated function.
* **Error Handling:** The Steering doc mandated `try/except` blocks around all file operations, which saved us during the "Windows Permission Error" crisis.

## 3. Vibe Coding (Problem Solving)
Kiro was instrumental in solving platform-specific bugs:
* **The Windows `WinError 183`:** When rewriting the `node_modules` folder, Windows file locking caused crashes. We used Vibe Coding to debug the traceback, and Kiro suggested the `shutil.copytree(..., dirs_exist_ok=True)` solution.
* **Regex Refactoring:** The `code_modernizer.py` module uses complex Regex to identify legacy `var` usage. Kiro generated these patterns, ensuring they didn't accidentally break valid code.

## 4. Impact Metrics
* **Development Velocity:** 14 days of work compressed into 4 days.
* **Code Quality:** 100% Type Safety coverage.
* **Automation:** The Kiro-generated modernizer refactored **74 files** in the `request` library demo in under 60 seconds.