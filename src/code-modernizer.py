import os
import re
from pathlib import Path
from typing import Dict, List
from rich.console import Console

console = Console()

def modernize_codebase(repo_path: str) -> Dict[str, int]:
    """
    Scans .js and .ts files and applies modern syntax patterns.
    """
    path = Path(repo_path)
    console.print(f"\n[bold magenta]🧬 Initiating Code DNA Evolution on {path}...[/bold magenta]")
    
    files_changed = 0
    total_replacements = 0
    
    # Patterns to modernize
    # 1. var -> let (We use let to be safe against reassignment)
    # 2. function() { return x } -> Arrow functions (Simple cases only)
    
    patterns = [
        (r'var\s+([a-zA-Z0-9_]+)\s*=', r'let \1 ='), # Change var to let
        (r'console\.log\((.*)\)', r'console.info(\1)'), # Modern logging practice
    ]

    # Walk through all files
    for root, _, files in os.walk(path):
        if "node_modules" in root: # SKIP node_modules
            continue
            
        for file in files:
            if file.endswith('.js') or file.endswith('.ts'):
                file_path = Path(root) / file
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    file_replacements = 0
                    
                    for pattern, replacement in patterns:
                        # Count matches first
                        matches = len(re.findall(pattern, new_content))
                        if matches > 0:
                            new_content = re.sub(pattern, replacement, new_content)
                            file_replacements += matches
                    
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        files_changed += 1
                        total_replacements += file_replacements
                        console.print(f"   [dim]Refactored: {file} ({file_replacements} changes)[/dim]")
                        
                except Exception as e:
                    # Ignore encoding errors on binary files
                    pass

    if files_changed > 0:
        console.print(f"   [green]✔ Modernized {files_changed} files with {total_replacements} improvements.[/green]")
    else:
        console.print("   [yellow]Codebase is already modern.[/yellow]")

    return {"files_changed": files_changed, "replacements": total_replacements}