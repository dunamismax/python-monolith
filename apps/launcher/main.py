"""
Python Monolith Central Launcher

A TUI application that automatically discovers and launches all Python applications
in the monorepo using uv for package management.
"""

import asyncio
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Static, Label, Button, Log, ProgressBar, 
    LoadingIndicator, OptionList
)
from textual.widgets.option_list import Option
from textual.binding import Binding
from textual.reactive import reactive
from textual.screen import Screen
from textual.message import Message
from rich.text import Text
from rich.console import Console


@dataclass
class AppInfo:
    """Information about a discovered Python application."""
    name: str
    path: Path
    type: str  # 'web', 'cli', 'tui', 'gui', 'script'
    main_file: Path
    description: str
    command: str
    port: Optional[int] = None


class AppDiscovery:
    """Discovers Python applications in the monorepo."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.console = Console()
    
    def discover_apps(self) -> List[AppInfo]:
        """Discover all Python applications in the repository."""
        apps = []
        
        # Scan the apps directory
        apps_dir = self.project_root / "apps"
        if apps_dir.exists():
            for app_path in apps_dir.iterdir():
                if app_path.is_dir() and app_path.name != "__pycache__":
                    app_info = self._analyze_app(app_path)
                    if app_info:
                        apps.append(app_info)
        
        # Scan scripts directory
        scripts_dir = self.project_root / "scripts"
        if scripts_dir.exists():
            for script_path in scripts_dir.glob("*.py"):
                if script_path.name != "__init__.py":
                    app_info = self._analyze_script(script_path)
                    if app_info:
                        apps.append(app_info)
        
        return sorted(apps, key=lambda x: (x.type, x.name))
    
    def _analyze_app(self, app_path: Path) -> Optional[AppInfo]:
        """Analyze an application directory to determine its type and details."""
        main_file = app_path / "main.py"
        if not main_file.exists():
            return None
        
        try:
            # Read the main file to determine app type and get description
            content = main_file.read_text(encoding='utf-8')
            
            app_type = self._determine_app_type(content, app_path)
            description = self._extract_description(content)
            command = self._generate_command(app_path, app_type)
            port = self._extract_port(content) if app_type == 'web' else None
            
            return AppInfo(
                name=app_path.name,
                path=app_path,
                type=app_type,
                main_file=main_file,
                description=description,
                command=command,
                port=port
            )
        except Exception as e:
            self.console.print(f"[red]Error analyzing {app_path}: {e}[/red]")
            return None
    
    def _analyze_script(self, script_path: Path) -> Optional[AppInfo]:
        """Analyze a script file."""
        try:
            content = script_path.read_text(encoding='utf-8')
            description = self._extract_description(content)
            
            return AppInfo(
                name=script_path.stem,
                path=script_path.parent,
                type='script',
                main_file=script_path,
                description=description,
                command=f"uv run python {script_path.relative_to(self.project_root)}"
            )
        except Exception as e:
            self.console.print(f"[red]Error analyzing {script_path}: {e}[/red]")
            return None
    
    def _determine_app_type(self, content: str, app_path: Path) -> str:
        """Determine the type of application based on its content and structure."""
        content_lower = content.lower()
        
        # Check for TUI frameworks first (more specific)
        if any(tui in content_lower for tui in ['from textual', 'import textual', 'textual.app', 'textual.widgets']):
            return 'tui'
        
        # Check for GUI frameworks
        if any(gui in content_lower for gui in ['from nicegui', 'import nicegui', 'nicegui', 'tkinter', 'pygame', 'kivy', 'pyside', 'pyqt']):
            return 'gui'
        
        # Check for CLI frameworks
        if any(cli in content_lower for cli in ['from typer', 'import typer', 'typer.typer', '@app.command', 'click.command', 'argparse.argumentparser']):
            return 'cli'
        
        # Check for web frameworks (FastAPI specifically)
        if any(framework in content_lower for framework in ['fastapi', 'from fastapi', 'flask', 'django', 'starlette']):
            return 'web'
        
        # Check directory structure clues
        if (app_path / "templates").exists() or (app_path / "static").exists():
            return 'web'
        
        return 'script'
    
    def _extract_description(self, content: str) -> str:
        """Extract description from docstring or comments."""
        lines = content.split('\n')
        
        # Look for module docstring
        in_docstring = False
        docstring_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            if not in_docstring and stripped.startswith('"""'):
                in_docstring = True
                if stripped.endswith('"""') and len(stripped) > 6:
                    return stripped[3:-3].strip()
                continue
            
            if in_docstring:
                if stripped.endswith('"""'):
                    break
                docstring_lines.append(stripped)
        
        if docstring_lines:
            return ' '.join(docstring_lines).strip()
        
        # Fallback to first comment
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#') and len(stripped) > 2:
                return stripped[1:].strip()
        
        return "Python application"
    
    def _extract_port(self, content: str) -> Optional[int]:
        """Extract port number from web application code."""
        import re
        
        # Look for common port patterns
        port_patterns = [
            r'port[=\s]*(\d+)',
            r'\.run\([^)]*port[=\s]*(\d+)',
            r'--port[=\s]*(\d+)',
            r'uvicorn.*:(\d+)',
        ]
        
        for pattern in port_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                try:
                    return int(matches[0])
                except ValueError:
                    continue
        
        return None
    
    def _generate_command(self, app_path: Path, app_type: str) -> str:
        """Generate the appropriate command to run the application."""
        relative_path = app_path.relative_to(self.project_root)
        
        if app_type == 'web':
            # Check if it's a FastAPI app
            main_content = (app_path / "main.py").read_text(encoding='utf-8')
            if 'fastapi' in main_content.lower():
                return f"uv run uvicorn {str(relative_path).replace('/', '.')}.main:app --reload"
            else:
                return f"uv run python -m {str(relative_path).replace('/', '.')}.main"
        
        elif app_type in ['cli', 'tui', 'gui']:
            return f"uv run python -m {str(relative_path).replace('/', '.')}.main"
        
        else:
            return f"uv run python {relative_path}/main.py"


class AppRunner:
    """Handles running applications with uv."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.running_processes: Dict[str, subprocess.Popen] = {}
    
    async def run_app(self, app_info: AppInfo) -> subprocess.Popen:
        """Run an application and return the process."""
        try:
            # Change to project root directory
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.project_root)
            
            # Split command into parts
            cmd_parts = app_info.command.split()
            
            # Start the process
            process = subprocess.Popen(
                cmd_parts,
                cwd=self.project_root,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.running_processes[app_info.name] = process
            return process
            
        except Exception as e:
            raise RuntimeError(f"Failed to start {app_info.name}: {e}")
    
    def stop_app(self, app_name: str) -> bool:
        """Stop a running application."""
        if app_name in self.running_processes:
            process = self.running_processes[app_name]
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            del self.running_processes[app_name]
            return True
        return False
    
    def is_running(self, app_name: str) -> bool:
        """Check if an application is currently running."""
        if app_name in self.running_processes:
            return self.running_processes[app_name].poll() is None
        return False


class RunningAppScreen(Screen):
    """Screen for monitoring a running application."""
    
    BINDINGS = [
        Binding("escape,q", "back", "Back to Launcher"),
        Binding("ctrl+c", "stop_app", "Stop App"),
    ]
    
    def __init__(self, app_info: AppInfo, runner: AppRunner):
        super().__init__()
        self.app_info = app_info
        self.runner = runner
        self.process: Optional[subprocess.Popen] = None
        self.log_widget: Optional[Log] = None
    
    def compose(self) -> ComposeResult:
        """Create the running app screen layout."""
        yield Header()
        
        with Container():
            yield Label(f"🚀 Running: {self.app_info.name}", id="app-title")
            yield Label(f"Type: {self.app_info.type.upper()}", id="app-type")
            yield Label(f"Command: {self.app_info.command}", id="app-command")
            
            if self.app_info.port:
                yield Label(f"🌐 URL: http://localhost:{self.app_info.port}", id="app-url")
            
            yield Label("📋 Output:", id="output-label")
            self.log_widget = Log(id="app-output")
            yield self.log_widget
        
        yield Footer()
    
    async def on_mount(self) -> None:
        """Start the application when the screen mounts."""
        try:
            self.process = await self.runner.run_app(self.app_info)
            self.set_timer(0.1, self._read_output)
            
            if self.app_info.type == 'web' and self.app_info.port:
                self.log_widget.write_line(f"🌐 Web app should be available at: http://localhost:{self.app_info.port}")
                
        except Exception as e:
            self.log_widget.write_line(f"❌ Failed to start application: {e}")
    
    def _read_output(self) -> None:
        """Read output from the running process."""
        if self.process and self.process.stdout:
            try:
                # Read available output without blocking
                line = self.process.stdout.readline()
                if line:
                    self.log_widget.write_line(line.rstrip())
                
                # Check if process is still running
                if self.process.poll() is not None:
                    self.log_widget.write_line(f"📋 Process exited with code: {self.process.returncode}")
                    return
                
                # Schedule next read
                self.set_timer(0.1, self._read_output)
                
            except Exception as e:
                self.log_widget.write_line(f"Error reading output: {e}")
    
    def action_back(self) -> None:
        """Return to the main launcher."""
        self.app.pop_screen()
    
    def action_stop_app(self) -> None:
        """Stop the running application."""
        if self.runner.stop_app(self.app_info.name):
            self.log_widget.write_line("🛑 Application stopped")
        else:
            self.log_widget.write_line("❌ Failed to stop application")


class MonolithLauncher(App):
    """Main launcher application."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #header {
        background: $primary;
        color: $text;
        text-align: center;
        height: 3;
        content-align: center middle;
        text-style: bold;
    }
    
    #subtitle {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }
    
    #app-list {
        border: solid $primary;
        height: 1fr;
        margin: 1;
    }
    
    #status {
        height: 3;
        background: $surface-lighten-1;
        padding: 1;
        border-top: solid $primary;
    }
    
    #loading {
        text-align: center;
        color: $primary;
        height: 1fr;
        content-align: center middle;
    }
    
    Button {
        margin: 1;
    }
    """
    
    TITLE = "🐍 Python Monolith Launcher"
    SUB_TITLE = "Central App Runner & Manager"
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("enter", "run_selected", "Run App"),
        Binding("ctrl+c", "quit", "Quit"),
    ]
    
    apps: reactive[List[AppInfo]] = reactive([])
    selected_index: reactive[int] = reactive(0)
    
    def __init__(self):
        super().__init__()
        self.project_root = Path(__file__).parent.parent.parent
        self.discovery = AppDiscovery(self.project_root)
        self.runner = AppRunner(self.project_root)
        self.app_list_widget: Optional[OptionList] = None
    
    def compose(self) -> ComposeResult:
        """Create the main launcher layout."""
        yield Header()
        
        with Container():
            yield Label("🐍 Python Monolith Launcher", id="header")
            yield Label("Discover and launch all Python applications", id="subtitle")
            
            with Container(id="loading"):
                yield LoadingIndicator()
                yield Label("Discovering applications...")
        
        yield Footer()
    
    async def on_mount(self) -> None:
        """Initialize the launcher when mounted."""
        await self.discover_apps()
    
    async def discover_apps(self) -> None:
        """Discover all applications in the repository."""
        try:
            # Run discovery in a thread to avoid blocking the UI
            apps = await asyncio.get_event_loop().run_in_executor(
                None, self.discovery.discover_apps
            )
            self.apps = apps
            await self.build_app_list()
            
        except Exception as e:
            self.apps = []
            # Remove loading indicator if it exists
            try:
                loading_container = self.query_one("#loading")
                await loading_container.remove()
            except:
                pass
            
            # Show error message
            error_msg = f"❌ Error discovering apps: {str(e)}"
            await self.mount(Label(error_msg, id="error"))
    
    async def build_app_list(self) -> None:
        """Build the application list widget."""
        # Remove loading indicator safely
        try:
            loading_container = self.query_one("#loading")
            await loading_container.remove()
        except Exception:
            # Loading container might already be removed or not exist
            pass
        
        # Create options for the OptionList
        options = []
        for i, app in enumerate(self.apps):
            type_icon = {
                'web': '🌐',
                'cli': '🖥️',
                'tui': '📱',
                'gui': '🖼️',
                'script': '📜'
            }.get(app.type, '📄')
            
            # Create option text
            option_text = f"{i+1}. {type_icon} {app.name} ({app.type.upper()})"
            subtitle = f"{app.description[:60]}..." if len(app.description) > 60 else app.description
            
            # Create Option - debug the text content
            if not option_text.strip():
                option_text = f"App {i+1}: {app.name if app.name else 'Unknown'}"
            
            options.append(Option(option_text, id=f"app-{i}"))
        
        # Create and mount OptionList
        self.app_list_widget = OptionList(*options, id="app-list")
        await self.mount(self.app_list_widget)
        
        # Add status bar
        status_text = f"Found {len(self.apps)} applications • Use ↑↓ to navigate, Enter to run, R to refresh, Q to quit"
        await self.mount(Label(status_text, id="status"))
        
        # Focus the list
        if self.apps:
            self.app_list_widget.focus()
    
    def action_refresh(self) -> None:
        """Refresh the application list."""
        # Clear existing widgets before refreshing
        try:
            if self.app_list_widget:
                self.app_list_widget.remove()
                self.app_list_widget = None
        except:
            pass
        
        try:
            status_widget = self.query_one("#status")
            status_widget.remove()
        except:
            pass
        
        asyncio.create_task(self.discover_apps())
    
    async def action_run_selected(self) -> None:
        """Run the currently selected application."""
        if not self.apps or not self.app_list_widget:
            # Show error if no apps or widget
            if hasattr(self, 'log_widget'):
                self.log_widget.write_line("No apps or widget available")
            return
        
        # Get the currently highlighted option index
        highlighted_index = self.app_list_widget.highlighted
        if highlighted_index is None or highlighted_index >= len(self.apps):
            # Create a temporary status message
            try:
                status_widget = self.query_one("#status", Label)
                status_widget.update("❌ No application selected or invalid selection")
            except:
                pass
            return
        
        selected_app = self.apps[highlighted_index]
        
        # Update status to show launching
        try:
            status_widget = self.query_one("#status", Label)
            status_widget.update(f"🚀 Launching {selected_app.name}...")
        except:
            pass
        
        # Push the running app screen
        running_screen = RunningAppScreen(selected_app, self.runner)
        self.push_screen(running_screen)
    
    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle option selection."""
        asyncio.create_task(self.action_run_selected())
    
    def on_key(self, event) -> None:
        """Handle key presses for debugging."""
        if event.key == "enter":
            # Make sure Enter key triggers app launch
            asyncio.create_task(self.action_run_selected())
            event.prevent_default()


def main():
    """Run the Python Monolith Launcher."""
    launcher = MonolithLauncher()
    launcher.run()


if __name__ == "__main__":
    main()