# 🐍 Python Monolith

A universal Python repository template for rapid development of web applications, command-line tools, terminal user interfaces (TUIs), graphical user interfaces (GUIs), scripts, and experiments. Built with modern Python tooling and best practices.

## 🎯 Philosophy

**One Repository, Many Apps** - This monolith serves as a unified home for all your Python projects, providing:

- **Shared Tooling**: Centralized development tools like `uv` for package management and `ruff` for code quality
- **Rapid Prototyping**: Pre-configured starter examples for each major application type
- **Clear Separation**: Logical directory structure keeping different applications isolated but accessible
- **Modern Stack**: Built with FastAPI, HTMX, Alpine.js, Typer, Textual, and NiceGUI

## 🏗️ Architecture

### Core Tech Stack

- **🌐 Web Framework**: FastAPI with HTMX and Alpine.js for hypermedia-driven applications
- **🎨 Styling**: Pico.css for elegant, class-less CSS styling
- **🖥️ CLI Framework**: Typer for powerful command-line interfaces
- **📱 TUI Framework**: Textual for sophisticated terminal applications
- **🖼️ GUI Framework**: NiceGUI for modern desktop and web GUI applications
- **🔧 Package Management**: `uv` for fast, reliable dependency management
- **✅ Code Quality**: `ruff` for linting and formatting

### Content Processing

- **python-markdown** - Markdown processing with extensions
- **python-frontmatter** - YAML frontmatter support
- **Pygments** - Syntax highlighting
- **pymdown-extensions** - Enhanced Markdown features

## 📁 Directory Structure

```
python-monolith/
├── apps/                    # Application modules
│   ├── launcher/           # 🚀 Central app launcher (NEW!)
│   │   └── main.py         # TUI launcher for all apps
│   ├── web/                # FastAPI + HTMX web applications
│   │   ├── main.py         # Web app entry point
│   │   ├── templates/      # Jinja2 templates
│   │   └── static/         # Static assets (CSS, JS, images)
│   ├── cli/                # Command-line applications
│   │   └── main.py         # CLI app entry point
│   ├── tui/                # Terminal user interfaces
│   │   └── main.py         # TUI app entry point
│   └── gui/                # GUI applications
│       └── main.py         # GUI app entry point
├── shared/                 # Shared utilities and modules
│   ├── __init__.py
│   └── utils.py           # Common utility functions
├── scripts/               # Standalone scripts
│   └── example_script.py  # Example utility script
├── tests/                 # Test modules
│   └── test_shared.py     # Tests for shared utilities
├── pyproject.toml         # Project configuration and dependencies
├── uv.lock               # Locked dependency versions
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone or download this repository**
2. **Create and activate a virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Verify installation** by running the central launcher (see section below)

## 🚀 Central Application Launcher

**The easiest way to run any application in this monorepo is through the central launcher!**

### Launch the TUI Launcher
```bash
uv run launcher
```
**OR**
```bash
uv run python -m apps.launcher.main
```

The launcher will:
- 🔍 **Auto-discover** all Python applications in the repository
- 📋 **Display** them in a beautiful numbered list with descriptions
- ⌨️ **Navigate** with arrow keys or numbers
- 🚀 **Launch** any app with Enter
- 📊 **Monitor** running applications with live output
- 🛑 **Stop** applications with Ctrl+C

### Launcher Features:
- **Smart Detection**: Automatically identifies web apps, CLI tools, TUIs, GUIs, and scripts
- **uv Integration**: All apps run through `uv` for consistent package management
- **Live Output**: See real-time output from running applications
- **Process Management**: Start and stop applications with ease
- **Keyboard Navigation**: Full keyboard control with intuitive shortcuts

### Keyboard Shortcuts:
- `↑↓` or `j k` - Navigate application list
- `Enter` - Launch selected application
- `q` - Quit launcher
- `r` - Refresh application list
- `Ctrl+C` - Stop running application (when viewing app output)
- `Escape` - Return to launcher from app output

## 🖥️ Manual Application Execution

You can also run applications manually if preferred:

### 🌐 Web Application (FastAPI + HTMX)

Start the web server:
```bash
uvicorn apps.web.main:app --reload --port 8000
```

Then open your browser to [http://localhost:8000](http://localhost:8000)

**Features demonstrated**:
- FastAPI with HTMX integration using FastHX
- Pico.css for beautiful, class-less styling
- Alpine.js for lightweight client-side reactivity
- Server-side partial updates with HTMX

### 🖥️ Command-Line Interface (Typer)

Run the CLI application:
```bash
python -m apps.cli.main hello --name "World"
```

**Available commands**:
```bash
python -m apps.cli.main hello --name "Python" --loud    # Greeting with options
python -m apps.cli.main info                            # Project information
python -m apps.cli.main version                         # Version information
python -m apps.cli.main --help                          # Show help
```

**Features demonstrated**:
- Type-safe command definitions with Typer
- Rich console output with panels and styling
- Option and argument handling
- Built-in help generation

### 📱 Terminal User Interface (Textual)

Launch the TUI application:
```bash
python -m apps.tui.main
```

**Keyboard shortcuts**:
- `q` - Quit application
- `h` - Show help
- `r` - Reset counter
- `Enter/Space` - Activate focused button

**Features demonstrated**:
- Modern terminal UI with Textual
- Reactive layouts and custom CSS styling
- Keyboard shortcuts and button interactions
- Real-time updates and state management

### 🖼️ GUI Application (NiceGUI)

Start the GUI application:
```bash
python -m apps.gui.main
```

The GUI will open in your default web browser at [http://localhost:8080](http://localhost:8080)

**Features demonstrated**:
- Modern web-based GUI with NiceGUI
- Interactive elements and real-time updates
- Custom CSS styling and responsive design
- Can be packaged as a desktop application

### 📜 Example Script

Run the utility script:
```bash
python scripts/example_script.py
```

**Features demonstrated**:
- Usage of shared utilities
- Logging configuration
- Configuration management
- File operations and hashing
- Performance timing

### ✅ Running Tests

Execute the test suite:
```bash
pytest tests/ -v
```

Or run a specific test file:
```bash
pytest tests/test_shared.py -v
```

## 🛠️ Development Tools

### Code Quality

**Format and lint code**:
```bash
ruff format .                    # Format code
ruff check .                     # Check for issues
ruff check . --fix              # Fix auto-fixable issues
```

**Type checking** (if mypy is installed):
```bash
mypy shared/ apps/
```

### Package Management

**Add new dependencies**:
```bash
uv add fastapi                   # Add to main dependencies
uv add --dev pytest             # Add to development dependencies
```

**Update dependencies**:
```bash
uv sync --upgrade               # Update all dependencies
uv lock --upgrade               # Update lock file
```

**Remove dependencies**:
```bash
uv remove package-name
```

## 🚀 Starting a New Project

### 1. Choose Your Application Type

Copy one of the starter templates from the `apps/` directory:

```bash
# For a new web app
cp -r apps/web apps/my-new-web-app

# For a new CLI tool
cp -r apps/cli apps/my-new-cli-tool

# For a new TUI app
cp -r apps/tui apps/my-new-tui-app

# For a new GUI app
cp -r apps/gui apps/my-new-gui-app
```

### 2. Customize Your Application

- Modify the `main.py` file in your new app directory
- Update templates, styles, and other assets as needed
- Add any specific dependencies to `pyproject.toml`

### 3. Use Shared Utilities

Import and use shared utilities in your application:

```python
from shared.utils import setup_logging, ConfigManager, Timer

# Setup logging
logger = setup_logging(level="INFO")

# Use configuration management
config = ConfigManager("my-app-config.json")
config.set("app.name", "My New App")

# Time operations
with Timer() as timer:
    # Your code here
    pass
logger.info(f"Operation took {timer.elapsed_time:.2f} seconds")
```

### 4. Add Tests

Create test files in the `tests/` directory:

```python
# tests/test_my_app.py
import pytest
from apps.my_app.main import my_function

def test_my_function():
    assert my_function("test") == "expected_result"
```

## 🔧 Configuration

### Environment Variables

Set these environment variables for different environments:

```bash
export PYTHON_ENV=development    # or production
export LOG_LEVEL=INFO           # DEBUG, INFO, WARNING, ERROR
export DATABASE_URL=sqlite:///./test.db
```

### Application Configuration

Each application can use the `ConfigManager` from shared utilities:

```python
from shared.utils import ConfigManager

config = ConfigManager("config.json")
config.set("database.host", "localhost")
config.set("database.port", 5432)
config.save()
```

## 📚 Shared Utilities Reference

The `shared/utils.py` module provides common functionality:

### Logging
```python
logger = setup_logging(level="INFO", log_file="app.log")
```

### Configuration Management
```python
config = ConfigManager("config.json")
config.set("key.nested", "value")
value = config.get("key.nested", default="fallback")
```

### File Operations
```python
file_hash = get_file_hash("path/to/file.txt", algorithm="sha256")
ensure_directory("path/to/directory")
```

### Performance Timing
```python
with Timer() as timer:
    # Your code here
    pass
print(f"Elapsed: {timer.elapsed_time:.2f}s")
```

### Environment Information
```python
env_info = get_environment_info()
print(f"Platform: {env_info['platform']}")
```

## 🤝 Contributing

1. **Format your code**: `ruff format .`
2. **Check for issues**: `ruff check . --fix`
3. **Run tests**: `pytest tests/ -v`
4. **Update documentation** as needed

## 📄 License

This project template is provided as-is for educational and development purposes.

## 🙋‍♂️ Support

For questions or issues:

1. Check the documentation in this README
2. Review the example applications in `apps/`
3. Look at the shared utilities in `shared/utils.py`
4. Run the tests to understand expected behavior

## 🎯 Quick Command Reference

### Central Launcher (Recommended)
```bash
uv run launcher                           # Launch the central TUI app launcher
```

### Individual Applications
```bash
# Web Applications
uv run uvicorn apps.web.main:app --reload --port 8000

# CLI Applications  
uv run python -m apps.cli.main hello --name "World"
uv run python -m apps.cli.main info
uv run python -m apps.cli.main --help

# TUI Applications
uv run python -m apps.tui.main
uv run python -m apps.launcher.main       # The launcher itself

# GUI Applications
uv run python -m apps.gui.main

# Scripts
uv run python scripts/example_script.py
```

### Development Tools
```bash
# Package Management
uv sync                                   # Install/sync dependencies
uv add package-name                       # Add new dependency

# Code Quality
ruff format .                             # Format code
ruff check . --fix                        # Lint and fix issues

# Testing
pytest tests/ -v                          # Run all tests
```

---

**Happy coding!** 🎉 This monolith template with its **central launcher** provides everything you need to rapidly prototype and develop Python applications across multiple domains. Simply run `uv run launcher` to get started!