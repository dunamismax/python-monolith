from textual.app import App, ComposeResult
from textual.containers import Center, Middle, Vertical
from textual.widgets import Button, Header, Footer, Static, Label
from textual.binding import Binding


class WelcomeScreen(Static):
    """A welcome screen widget."""
    
    def compose(self) -> ComposeResult:
        yield Label("🐍 Welcome to Python Monolith TUI!", id="title")
        yield Label("Built with Textual for modern terminal interfaces", id="subtitle")
        yield Label("", id="status")


class MonolithTUI(App):
    """A simple Textual TUI application for the Python Monolith."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #title {
        text-align: center;
        text-style: bold;
        color: $primary;
        margin: 1;
    }
    
    #subtitle {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }
    
    #status {
        text-align: center;
        margin: 1;
        height: 3;
    }
    
    Button {
        margin: 1;
        min-width: 20;
    }
    
    .success {
        color: $success;
        text-style: bold;
    }
    
    .info {
        color: $info;
    }
    
    Vertical {
        align: center middle;
        height: auto;
    }
    """
    
    TITLE = "Python Monolith TUI"
    SUB_TITLE = "Universal Python Repository"
    
    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("h", "show_help", "Help"),
        Binding("r", "reset", "Reset"),
    ]
    
    def __init__(self) -> None:
        super().__init__()
        self.click_count = 0
    
    def compose(self) -> ComposeResult:
        """Create the TUI layout."""
        yield Header()
        yield Center(
            Middle(
                Vertical(
                    WelcomeScreen(),
                    Button("Click Me!", id="click-btn", variant="primary"),
                    Button("Show Info", id="info-btn", variant="default"),
                    Button("Quit Application", id="quit-btn", variant="error"),
                    id="main-container"
                )
            )
        )
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        status_widget = self.query_one("#status", Label)
        
        if event.button.id == "click-btn":
            self.click_count += 1
            status_widget.update(f"Button clicked {self.click_count} time(s)! ✨")
            status_widget.add_class("success")
            
        elif event.button.id == "info-btn":
            info_text = """
This TUI demonstrates:
• Modern terminal interfaces with Textual
• Reactive layouts and styling
• Keyboard shortcuts and button interactions
• Integration with the Python Monolith ecosystem
            """.strip()
            status_widget.update(info_text)
            status_widget.add_class("info")
            
        elif event.button.id == "quit-btn":
            self.exit()
    
    def action_show_help(self) -> None:
        """Show help information."""
        help_text = """
Keyboard Shortcuts:
• q - Quit application
• h - Show this help
• r - Reset counter
• Enter/Space - Activate focused button
        """.strip()
        status_widget = self.query_one("#status", Label)
        status_widget.update(help_text)
        status_widget.add_class("info")
    
    def action_reset(self) -> None:
        """Reset the click counter."""
        self.click_count = 0
        status_widget = self.query_one("#status", Label)
        status_widget.update("Counter reset! 🔄")
        status_widget.add_class("success")
    
    def action_quit(self) -> None:
        """Quit the application."""
        self.exit()


def main() -> None:
    """Run the TUI application."""
    app = MonolithTUI()
    app.run()


if __name__ == "__main__":
    main()