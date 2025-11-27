"""
Dependency Manager module for updating npm/yarn dependencies.
Handles semantic versioning logic and package updates.
"""

import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import aiohttp
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


@dataclass
class UpdateInfo:
    """Information about a dependency update."""
    package: str
    current_version: str
    latest_version: str
    update_type: str  # 'major', 'minor', 'patch'


@dataclass
class UpdateResult:
    """Result of updating dependencies."""
    repo_path: Path
    updates_applied: List[UpdateInfo]
    backup_created: bool
    errors: List[str]
    success: bool


class DependencyManager:
    """Manages npm/yarn dependency updates with semantic versioning."""
    
    def __init__(self, repo_path: str):
        """
        Initialize the dependency manager.
        
        Args:
            repo_path: Path to the repository
        """
        self.repo_path = Path(repo_path)
        self.package_json_path = self.repo_path / "package.json"
        self.backup_path = self.repo_path / "package.json.backup"
    
    async def update_dependencies(self) -> UpdateResult:
        """
        Update all dependencies to their latest compatible versions.
        
        Returns:
            UpdateResult containing update information
        """
        errors: List[str] = []
        updates_applied: List[UpdateInfo] = []
        
        # Verify package.json exists
        if not self.package_json_path.exists():
            errors.append(f"package.json not found at {self.package_json_path}")
            return UpdateResult(
                repo_path=self.repo_path,
                updates_applied=[],
                backup_created=False,
                errors=errors,
                success=False
            )
        
        # Create backup
        try:
            backup_created = self._create_backup()
        except Exception as e:
            errors.append(f"Failed to create backup: {str(e)}")
            return UpdateResult(
                repo_path=self.repo_path,
                updates_applied=[],
                backup_created=False,
                errors=errors,
                success=False
            )
        
        # Load package.json
        try:
            package_data = self._load_package_json()
        except Exception as e:
            errors.append(f"Failed to load package.json: {str(e)}")
            return UpdateResult(
                repo_path=self.repo_path,
                updates_applied=[],
                backup_created=backup_created,
                errors=errors,
                success=False
            )
        
        # Get latest versions
        try:
            updates_applied = await self._get_and_apply_updates(package_data)
        except Exception as e:
            errors.append(f"Failed to update dependencies: {str(e)}")
            self._restore_backup()
            return UpdateResult(
                repo_path=self.repo_path,
                updates_applied=[],
                backup_created=backup_created,
                errors=errors,
                success=False
            )
        
        # Save updated package.json
        try:
            self._save_package_json(package_data)
        except Exception as e:
            errors.append(f"Failed to save package.json: {str(e)}")
            self._restore_backup()
            return UpdateResult(
                repo_path=self.repo_path,
                updates_applied=[],
                backup_created=backup_created,
                errors=errors,
                success=False
            )
        
        # Run npm install
        try:
            await self._run_npm_install()
        except Exception as e:
            errors.append(f"npm install failed: {str(e)}")
            self._restore_backup()
            return UpdateResult(
                repo_path=self.repo_path,
                updates_applied=updates_applied,
                backup_created=backup_created,
                errors=errors,
                success=False
            )
        
        console.print(f"[green]✓[/green] Successfully updated {len(updates_applied)} dependencies")
        
        return UpdateResult(
            repo_path=self.repo_path,
            updates_applied=updates_applied,
            backup_created=backup_created,
            errors=errors,
            success=True
        )

    def _create_backup(self) -> bool:
        """Create a backup of package.json."""
        with console.status("[bold yellow]Creating backup..."):
            try:
                import shutil
                shutil.copy2(self.package_json_path, self.backup_path)
                console.print(f"[green]✓[/green] Backup created at {self.backup_path}")
                return True
            except Exception as e:
                raise Exception(f"Backup failed: {str(e)}")
    
    def _restore_backup(self) -> None:
        """Restore package.json from backup."""
        try:
            if self.backup_path.exists():
                import shutil
                shutil.copy2(self.backup_path, self.package_json_path)
                console.print("[yellow]⚠[/yellow] Restored from backup")
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to restore backup: {str(e)}")
    
    def _load_package_json(self) -> Dict:
        """Load and parse package.json."""
        try:
            with open(self.package_json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to read file: {str(e)}")
    
    def _save_package_json(self, data: Dict) -> None:
        """Save package.json with proper formatting."""
        try:
            with open(self.package_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')  # Add trailing newline
        except Exception as e:
            raise Exception(f"Failed to write file: {str(e)}")
    
    async def _get_and_apply_updates(self, package_data: Dict) -> List[UpdateInfo]:
        """
        Get latest versions and update package.json.
        
        Args:
            package_data: Parsed package.json data
            
        Returns:
            List of UpdateInfo objects
        """
        updates: List[UpdateInfo] = []
        
        # Collect all dependencies
        all_deps: List[Tuple[str, str, str]] = []  # (name, version, dep_type)
        
        if 'dependencies' in package_data:
            for name, version in package_data['dependencies'].items():
                all_deps.append((name, version, 'dependencies'))
        
        if 'devDependencies' in package_data:
            for name, version in package_data['devDependencies'].items():
                all_deps.append((name, version, 'devDependencies'))
        
        if not all_deps:
            console.print("[yellow]No dependencies to update[/yellow]")
            return updates
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(
                "[cyan]Checking for updates...", 
                total=len(all_deps)
            )
            
            async with aiohttp.ClientSession() as session:
                for name, current_version, dep_type in all_deps:
                    try:
                        latest_version = await self._get_latest_version(session, name)
                        
                        if latest_version and latest_version != current_version.lstrip('^~'):
                            # Update in package_data
                            package_data[dep_type][name] = f"^{latest_version}"
                            
                            update_type = self._determine_update_type(
                                current_version.lstrip('^~'),
                                latest_version
                            )
                            
                            updates.append(UpdateInfo(
                                package=name,
                                current_version=current_version,
                                latest_version=latest_version,
                                update_type=update_type
                            ))
                    except Exception as e:
                        console.print(f"[yellow]⚠[/yellow] Error checking {name}: {str(e)}")
                    
                    progress.advance(task)
        
        return updates
    
    async def _get_latest_version(
        self, 
        session: aiohttp.ClientSession, 
        package_name: str
    ) -> Optional[str]:
        """
        Get the latest version of a package from NPM registry.
        
        Args:
            session: aiohttp session
            package_name: Name of the package
            
        Returns:
            Latest version string or None
        """
        try:
            url = f"https://registry.npmjs.org/{package_name}/latest"
            
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 200:
                    return None
                
                data = await response.json()
                return data.get('version')
                
        except Exception:
            return None
    
    def _determine_update_type(self, current: str, latest: str) -> str:
        """
        Determine if update is major, minor, or patch.
        
        Args:
            current: Current version
            latest: Latest version
            
        Returns:
            'major', 'minor', or 'patch'
        """
        try:
            current_parts = [int(x) for x in current.split('.')]
            latest_parts = [int(x) for x in latest.split('.')]
            
            if current_parts[0] != latest_parts[0]:
                return 'major'
            elif current_parts[1] != latest_parts[1]:
                return 'minor'
            else:
                return 'patch'
        except Exception:
            return 'unknown'
    
    async def _run_npm_install(self) -> None:
        """Run npm install to update node_modules."""
        with console.status("[bold cyan]Running npm install..."):
            try:
                process = await asyncio.create_subprocess_exec(
                    'npm', 'install',
                    cwd=self.repo_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await process.communicate()
                
                if process.returncode != 0:
                    error_msg = stderr.decode() if stderr else "Unknown error"
                    raise Exception(f"npm install failed: {error_msg}")
                
                console.print("[green]✓[/green] npm install completed")
                
            except FileNotFoundError:
                raise Exception("npm not found. Please install Node.js and npm.")
            except Exception as e:
                raise Exception(f"npm install error: {str(e)}")


async def update_repository_dependencies(repo_path: str) -> UpdateResult:
    """
    Convenience function to update repository dependencies.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        UpdateResult object
    """
    manager = DependencyManager(repo_path)
    return await manager.update_dependencies()
