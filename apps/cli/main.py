import typer
from rich import print
from rich.console import Console
from rich.panel import Panel
from typing import Optional

app = typer.Typer(
    name="monolith-cli",
    help="Python Monolith CLI application built with Typer",
    add_completion=False,
)
console = Console()


@app.command()
def hello(
    name: Optional[str] = typer.Option(
        "World", 
        "--name", 
        "-n", 
        help="Name to greet"
    ),
    loud: bool = typer.Option(
        False, 
        "--loud", 
        "-l", 
        help="Make the greeting louder"
    ),
) -> None:
    """
    Say hello to someone with style.
    """
    greeting = f"Hello, {name}!"
    
    if loud:
        greeting = greeting.upper() + " 🎉"
    
    console.print(
        Panel(
            greeting,
            title="🐍 Python Monolith CLI",
            title_align="center",
            border_style="blue",
            padding=(1, 2),
        )
    )


@app.command()
def info() -> None:
    """
    Display information about the Python Monolith project.
    """
    info_text = """
[bold blue]Python Monolith Repository[/bold blue]

A universal starter template for Python projects including:
• 🌐 Web applications (FastAPI + HTMX)
• 🖥️  Command-line tools (Typer)
• 📱 Terminal UIs (Textual)
• 🖼️  GUI applications (NiceGUI)
• 📜 Scripts and experiments

[bold green]Built with modern Python tooling:[/bold green]
• uv for package management
• ruff for code quality
• Rich for beautiful CLI output
    """
    
    console.print(Panel(info_text, border_style="green"))


@app.command()
def version() -> None:
    """
    Show the current version.
    """
    print("[bold blue]Python Monolith CLI v0.1.0[/bold blue]")


if __name__ == "__main__":
    app()