import subprocess
import os
from pathlib import Path
from typing import List, Dict
from rich.console import Console

console = Console()

def update_dependencies(repo_path: str, outdated_deps: List[Dict]) -> Dict[str, List[str]]:
    """
    Iterates through outdated dependencies and runs 'npm install <pkg>@latest'.
    Includes aggressive fallback strategies for dead projects.
    """
    path = Path(repo_path)
    success = []
    failed = []
    
    console.print(f"\n[bold magenta]⚡ Starting Resurrection Sequence on {path}...[/bold magenta]")
    
    # Strategy 1: Nuke the lockfile.
    lockfile = path / "package-lock.json"
    if lockfile.exists():
        console.print("   [dim]🔓 Breaking existing lockfile chains...[/dim]")
        os.remove(lockfile)

    for dep in outdated_deps:
        if dep['status'] != "Outdated":
            continue

        pkg_name = dep['name']
        target_version = dep['latest']
        
        console.print(f"   💉 Injecting life into [cyan]{pkg_name}[/cyan] (Target: {target_version})...", end="")
        
        # FLAG EXPLANATION:
        # --save-exact: Lock the new version
        # --no-audit: Don't waste time checking security yet
        # --ignore-scripts: CRITICAL. Prevents old 'postinstall' scripts from crashing.
        base_cmd = f"npm install {pkg_name}@latest --save-exact --no-audit --ignore-scripts"
        
        try:
            # Attempt 1: Standard Install (with ignore-scripts)
            subprocess.check_output(
                base_cmd, 
                cwd=str(path), 
                shell=True,
                stderr=subprocess.STDOUT 
            )
            console.print(" [green]SUCCESS[/green]")
            success.append(pkg_name)
            
        except subprocess.CalledProcessError as e:
            # Attempt 2: FORCE Install (The "Defibrillator" Shot)
            try:
                force_cmd = f"{base_cmd} --force --legacy-peer-deps"
                subprocess.check_output(
                    force_cmd, 
                    cwd=str(path), 
                    shell=True,
                    stderr=subprocess.STDOUT
                )
                console.print(" [green]SUCCESS (FORCED)[/green]")
                success.append(pkg_name)
            except subprocess.CalledProcessError as e2:
                console.print(" [red]FAILED[/red]")
                # PRINT THE ACTUAL ERROR so we can see what happened
                error_msg = e2.output.decode('utf-8', errors='ignore').split('\n')[0]
                console.print(f"      [dim red]Reason: {error_msg[:100]}...[/dim red]")
                failed.append(pkg_name)
        except Exception as e:
            console.print(f" [red]ERROR: {e}[/red]")
            failed.append(pkg_name)

    return {"success": success, "failed": failed}