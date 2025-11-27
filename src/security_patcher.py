import subprocess
import json
from pathlib import Path
from typing import Dict, Any
from rich.console import Console

console = Console()

def get_security_report(repo_path: Path) -> Dict[str, Any]:
    """Runs npm audit to get the current vulnerability state."""
    try:
        # Run npm audit --json to get raw data
        # We use shell=True for Windows compatibility
        result = subprocess.run(
            "npm audit --json", 
            cwd=str(repo_path), 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        # npm audit returns non-zero exit code if vulnerabilities found,
        # so we don't check_returncode() here.
        output = result.stdout.decode('utf-8', errors='ignore')
        
        if not output.strip():
            return {"vulnerabilities": {}, "metadata": {"totalDependencies": 0}}

        data = json.loads(output)
        return data
    except Exception as e:
        console.print(f"[dim red]Could not generate security report: {e}[/dim red]")
        return {}

def patch_security(repo_path: str) -> Dict[str, int]:
    """
    The Security Exorcist.
    Runs 'npm audit fix --force' to crush vulnerabilities.
    """
    path = Path(repo_path)
    console.print(f"\n[bold magenta]🛡️  Initiating Security Protocol on {path}...[/bold magenta]")
    
    # 1. Scan Before
    console.print("   [cyan]Scanning for vulnerabilities...[/cyan]")
    before_report = get_security_report(path)
    vuln_counts = before_report.get('metadata', {}).get('vulnerabilities', {})
    total_vulns = sum(vuln_counts.values()) if vuln_counts else 0
    
    if total_vulns == 0:
        console.print("   [green]No vulnerabilities found. The vessel is pure.[/green]")
        return {"fixed": 0, "remaining": 0}

    console.print(f"   [red]⚠️  DETECTED {total_vulns} VULNERABILITIES![/red]")
    console.print(f"      Critical: {vuln_counts.get('critical', 0)}")
    console.print(f"      High:     {vuln_counts.get('high', 0)}")

    # 2. Attempt Fix
    console.print("   [yellow]💉 Applying Security Patches (npm audit fix)...[/yellow]")
    try:
        # --force is necessary to update locked transitive dependencies
        subprocess.run(
            "npm audit fix --force", 
            cwd=str(path), 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        console.print("   [green]✔ Patches Applied.[/green]")
    except Exception as e:
        console.print(f"   [red]Patching Failed: {e}[/red]")

    # 3. Scan After (Verification)
    after_report = get_security_report(path)
    after_counts = after_report.get('metadata', {}).get('vulnerabilities', {})
    remaining_vulns = sum(after_counts.values()) if after_counts else 0
    
    fixed_count = total_vulns - remaining_vulns
    
    if fixed_count > 0:
        console.print(f"   [bold green]✨ SUCCESS: Eliminated {fixed_count} security threats.[/bold green]")
    
    if remaining_vulns > 0:
        console.print(f"   [bold red]💀 WARNING: {remaining_vulns} vulnerabilities remain (Manual Review Required).[/bold red]")
    else:
        console.print("   [bold green]🛡️  Security Status: SECURE[/bold green]")

    return {"fixed": fixed_count, "remaining": remaining_vulns}