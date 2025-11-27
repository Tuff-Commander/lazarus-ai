import json
import shutil
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import requests
import git
from rich.console import Console

console = Console()

class InvalidProjectError(Exception):
    """Raised when the repository is not a valid target."""
    pass

def get_latest_version(package_name: str) -> Optional[str]:
    """Fetches the latest version of a package from the npm registry."""
    try:
        response = requests.get(f"https://registry.npmjs.org/{package_name}/latest", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("version")
    except Exception:
        return None
    return None

def scan_repository(repo_url: str, cleanup: bool = True) -> Dict[str, Any]:
    """
    Clones a repository and analyzes its health.
    If cleanup=False, it leaves the cloned files for the Resurrect engine to use.
    """
    # Create a temp dir that persists if we need it
    temp_dir = Path(tempfile.mkdtemp(prefix="lazarus_scan_"))
    
    try:
        console.print(f"[bold blue]📡 Cloning {repo_url}...[/bold blue]")
        
        try:
            repo = git.Repo.clone_from(repo_url, temp_dir, depth=1)
        except git.GitCommandError as e:
            raise InvalidProjectError(f"Failed to clone repository: {str(e)}")

        package_json_path = temp_dir / "package.json"
        if not package_json_path.exists():
            raise InvalidProjectError("No package.json found. Is this a Node.js project?")

        with open(package_json_path, "r", encoding="utf-8") as f:
            package_data = json.load(f)

        dependencies = package_data.get("dependencies", {})
        dev_dependencies = package_data.get("devDependencies", {})
        all_deps = {**dependencies, **dev_dependencies}

        console.print(f"[bold yellow]🔍 Analyzing {len(all_deps)} dependencies...[/bold yellow]")
        
        outdated_count = 0
        analyzed_deps = []

        # Limit scanning to first 20 deps for speed
        for name, current_version in list(all_deps.items())[:20]: 
            latest = get_latest_version(name)
            status = "Current"
            
            # Basic check (ignoring ^ and ~ for MVP speed)
            clean_current = current_version.replace("^", "").replace("~", "")
            if latest and clean_current != latest:
                outdated_count += 1
                status = "Outdated"

            analyzed_deps.append({
                "name": name,
                "current": current_version,
                "latest": latest,
                "status": status
            })

        total_deps = len(analyzed_deps)
        if total_deps > 0:
            health_ratio = (total_deps - outdated_count) / total_deps
            resurrection_score = int(health_ratio * 100)
        else:
            resurrection_score = 100

        report = {
            "repo_url": repo_url,
            "local_path": str(temp_dir), # CRITICAL: Pass this path to the Resurrector
            "project_name": package_data.get("name", "Unknown"),
            "resurrection_score": resurrection_score,
            "dependency_health": {
                "total": len(all_deps),
                "outdated": outdated_count,
                "details": analyzed_deps
            }
        }
        
        return report

    except Exception as e:
        # If scan fails, always cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise e
    finally:
        # Only cleanup if explicitly asked
        if cleanup:
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass