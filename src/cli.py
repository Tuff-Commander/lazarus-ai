import click
import shutil
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from scanner import scan_repository, InvalidProjectError
from dependency_manager import update_dependencies
from security_patcher import patch_security
# NEW IMPORT
from code_modernizer import modernize_codebase

console = Console()

@click.group()
def cli():
    """🧟 Lazarus AI - Resurrection Engine"""
    pass

def display_report(report):
    """Helper to print the table"""
    table = Table(title="💀 Project Death Report")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_row("Project Name", report['project_name'])
    table.add_row("Resurrection Score", f"{report['resurrection_score']}/100")
    table.add_row("Total Dependencies", str(report['dependency_health']['total']))
    table.add_row("Outdated Dependencies", str(report['dependency_health']['outdated']))
    console.print(table)
    
    if report['dependency_health']['outdated'] > 0:
        console.print("\n[bold red]⚠️  Critical Decay Detected:[/bold red]")
        for dep in report['dependency_health']['details']:
            if dep['status'] == "Outdated":
                console.print(f" - [yellow]{dep['name']}[/yellow]: {dep['current']} -> [green]{dep['latest']}[/green]")

@cli.command()
@click.argument('repo_url')
def scan(repo_url):
    """Scans a repository (and cleans up afterwards)."""
    console.print(Panel(f"[bold green]Summoning Lazarus AI...[/bold green]\nTarget: {repo_url}"))
    try:
        # cleanup=True because we just want to look, not touch
        report = scan_repository(repo_url, cleanup=True)
        display_report(report)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")

@cli.command()
@click.argument('repo_url')
def resurrect(repo_url):
    """Scans AND attempts to fix the repository."""
    console.print(Panel(f"[bold magenta]Attempting Resurrection...[/bold magenta]\nTarget: {repo_url}"))
    
    local_path = None
    try:
        # 1. SCAN
        report = scan_repository(repo_url, cleanup=False)
        local_path = report['local_path']
        display_report(report)

        if report['dependency_health']['outdated'] == 0:
            console.print("[green]This project is already alive! No action needed.[/green]")
            return

        # 2. CONFIRMATION
        if click.confirm('\n⚡ Do you want to attempt resurrection?'):
            
            # 3. DEPENDENCY UPDATES
            results = update_dependencies(
                local_path, 
                report['dependency_health']['details']
            )
            
            # 4. SECURITY PATCHING
            console.print("\n")
            patch_results = patch_security(local_path)

            # 5. CODE MODERNIZATION (NEW)
            console.print("\n")
            modernize_results = modernize_codebase(local_path)
            
            # 6. FINAL SUMMARY
            console.print(Panel(
                f"[bold green]Resurrection Complete![/bold green]\n"
                f"📦 Dependencies Updated: {len(results['success'])}\n"
                f"🛡️  Security Holes Patched: {patch_results['fixed']}\n"
                f"🧬 Files Modernized: {modernize_results['files_changed']} ({modernize_results['replacements']} patterns)"
            ))
            
            console.print(f"\n[dim]Project is revived at: {local_path}[/dim]")
            console.print("[bold]Warning:[/bold] This is a temp folder. Copy it elsewhere if you want to keep it!")
        else:
            console.print("Resurrection aborted.")
            
    except Exception as e:
        console.print(f"[bold red]Resurrection Failed:[/bold red] {str(e)}")
    finally:
        pass

if __name__ == '__main__':
    cli()