import os
import re
from pathlib import Path
from typing import Dict, Any, List
from rich.console import Console

console = Console()

def modernize_codebase(repo_path: str) -> Dict[str, Any]:
    """
    Scans .js and .ts files and applies modern syntax patterns.
    Returns details on exactly WHICH files were changed.
    """
    path = Path(repo_path)
    console.print(f"\n[bold magenta]🧬 Initiating Code DNA Evolution on {path}...[/bold magenta]")
    
    modified_files = [] # Store names of changed files
    total_replacements = 0
    
    # Patterns to modernize
    patterns = [
        (r'var\s+([a-zA-Z0-9_]+)\s*=', r'let \1 ='), 
        (r'console\.log\((.*)\)', r'console.info(\1)'),
    ]

    for root, _, files in os.walk(path):
        if "node_modules" in root: continue
            
        for file in files:
            if file.endswith(('.js', '.ts', '.jsx', '.tsx')):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    file_replacements = 0
                    
                    for pattern, replacement in patterns:
                        matches = len(re.findall(pattern, new_content))
                        if matches > 0:
                            new_content = re.sub(pattern, replacement, new_content)
                            file_replacements += matches
                    
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        modified_files.append(file) # Track the filename
                        total_replacements += file_replacements
                        console.print(f"   [dim]Refactored: {file}[/dim]")
                        
                except Exception:
                    pass

    return {
        "files_changed": len(modified_files), 
        "file_names": modified_files, # <--- THIS FIXES YOUR ERROR
        "replacements": total_replacements
    }