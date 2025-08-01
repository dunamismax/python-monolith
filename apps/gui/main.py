from nicegui import ui, app
import asyncio
from datetime import datetime


class MonolithGUI:
    """Main GUI application class for Python Monolith."""
    
    def __init__(self):
        self.click_count = 0
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the GUI interface."""
        # Configure the page
        ui.page_title("Python Monolith GUI")
        
        # Add custom CSS
        ui.add_head_html("""
        <style>
            .main-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 2rem;
            }
            .card {
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                padding: 2rem;
                margin: 1rem 0;
            }
            .gradient-bg {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
        </style>
        """)
        
        # Main container
        with ui.element('div').classes('gradient-bg'):
            with ui.element('div').classes('main-container'):
                # Header
                with ui.element('div').classes('card'):
                    ui.html('<h1 style="text-align: center; margin: 0; color: #333;">🐍 Python Monolith GUI</h1>')
                    ui.html('<p style="text-align: center; color: #666; margin: 0.5rem 0 0 0;">Built with NiceGUI for modern Python desktop applications</p>')
                
                # Interactive demo section
                with ui.element('div').classes('card'):
                    ui.label('Interactive Demo').style('font-size: 1.5rem; font-weight: bold; color: #333; margin-bottom: 1rem;')
                    
                    # Status label
                    self.status_label = ui.label('Welcome! Click the buttons below to interact.').style('color: #666; margin-bottom: 1rem;')
                    
                    # Click counter
                    with ui.row().style('gap: 1rem; margin-bottom: 1rem;'):
                        ui.button('Click Me!', on_click=self.on_button_click).props('color=primary')
                        ui.button('Reset Counter', on_click=self.reset_counter).props('color=secondary')
                    
                    self.click_label = ui.label(f'Button clicked: {self.click_count} times').style('font-weight: bold;')
                
                # Input demo section
                with ui.element('div').classes('card'):
                    ui.label('Input Demo').style('font-size: 1.5rem; font-weight: bold; color: #333; margin-bottom: 1rem;')
                    
                    self.name_input = ui.input('Enter your name', placeholder='Your name here...').style('margin-bottom: 1rem;')
                    ui.button('Greet Me!', on_click=self.greet_user).props('color=positive')
                    
                    self.greeting_label = ui.label('').style('font-size: 1.2rem; color: #2e7d32; margin-top: 1rem;')
                
                # Features section
                with ui.element('div').classes('card'):
                    ui.label('Python Monolith Features').style('font-size: 1.5rem; font-weight: bold; color: #333; margin-bottom: 1rem;')
                    
                    features = [
                        "🌐 Web Applications (FastAPI + HTMX)",
                        "🖥️ Command-line Tools (Typer)",
                        "📱 Terminal UIs (Textual)",
                        "🖼️ GUI Applications (NiceGUI)",
                        "📜 Scripts and Experiments",
                        "🔧 Shared Utilities and Tooling"
                    ]
                    
                    for feature in features:
                        ui.label(feature).style('margin: 0.5rem 0; color: #555;')
                
                # Real-time clock
                with ui.element('div').classes('card'):
                    ui.label('Real-time Clock').style('font-size: 1.5rem; font-weight: bold; color: #333; margin-bottom: 1rem;')
                    self.clock_label = ui.label('').style('font-size: 1.5rem; color: #1976d2; font-family: monospace;')
                
                # Footer
                with ui.element('div').classes('card'):
                    ui.html('<p style="text-align: center; color: #666; margin: 0;">Built with ❤️ using NiceGUI and Python</p>')
        
        # Start the clock
        ui.timer(1.0, self.update_clock)
    
    def on_button_click(self):
        """Handle button click events."""
        self.click_count += 1
        self.click_label.text = f'Button clicked: {self.click_count} times'
        self.status_label.text = f'Great! You clicked the button. Total clicks: {self.click_count} 🎉'
    
    def reset_counter(self):
        """Reset the click counter."""
        self.click_count = 0
        self.click_label.text = f'Button clicked: {self.click_count} times'
        self.status_label.text = 'Counter has been reset! ✨'
    
    def greet_user(self):
        """Greet the user with their entered name."""
        name = self.name_input.value.strip()
        if name:
            greeting = f'Hello, {name}! Welcome to the Python Monolith GUI! 👋'
            self.greeting_label.text = greeting
            self.status_label.text = f'Nice to meet you, {name}!'
        else:
            self.greeting_label.text = 'Please enter your name first! 😊'
            self.status_label.text = 'Don\'t be shy, tell us your name!'
    
    def update_clock(self):
        """Update the real-time clock."""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.clock_label.text = current_time


def main():
    """Run the GUI application."""
    # Initialize the GUI
    gui = MonolithGUI()
    
    # Configure NiceGUI
    ui.run(
        title='Python Monolith GUI',
        native=False,  # Set to True to run as desktop app
        port=8080,
        show=True,
        reload=False
    )


if __name__ == "__main__":
    main()