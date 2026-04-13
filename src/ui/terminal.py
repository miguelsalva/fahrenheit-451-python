"""Terminal UI for Fahrenheit 451."""

import sys
from typing import Optional
from io import StringIO

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.syntax import Syntax
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class TerminalUI:
    """Terminal UI for Fahrenheit 451 adventure game."""
    
    def __init__(self):
        self.console: Optional[Console] = None
        if RICH_AVAILABLE:
            self.console = Console(width=80)
    
    def print_title(self, title: str) -> None:
        """Print game title."""
        if RICH_AVAILABLE and self.console:
            text = Text(title, style="bold cyan")
            self.console.print(Panel(text, border_style="bright_blue"))
        else:
            print(title)
    
    def print_text(self, text: str, style: str = "") -> None:
        """Print regular text."""
        if RICH_AVAILABLE and self.console:
            if style:
                self.console.print(text, style=style)
            else:
                self.console.print(text)
        else:
            print(text)
    
    def print_message(self, message: str) -> None:
        """Print a game message."""
        if RICH_AVAILABLE and self.console:
            self.console.print(message, style="white")
        else:
            print(message)
    
    def print_error(self, error: str) -> None:
        """Print an error message."""
        if RICH_AVAILABLE and self.console:
            self.console.print(f"[red]Error:[/red] {error}")
        else:
            print(f"Error: {error}")
    
    def print_room(self, room_name: str, description: str, exits: str) -> None:
        """Print room information."""
        if RICH_AVAILABLE and self.console:
            header = Text(room_name, style="bold yellow")
            desc_text = Text(description, style="white")
            exit_text = Text(f"\n{exits}", style="dim cyan")
            
            full_text = Text.assemble(desc_text, "\n", exit_text)
            self.console.print(Panel(full_text, title=str(header), 
                                    border_style="bright_yellow"))
        else:
            print(f"\n{room_name}\n")
            print(description)
            print(f"\n{exits}")
    
    def print_inventory(self, items: list[str]) -> None:
        """Print inventory contents."""
        if RICH_AVAILABLE and self.console:
            if items:
                item_list = "\n".join(f"  • {item}" for item in items)
                self.console.print(Panel(item_list, title="[bold]Inventory[/bold]",
                                        border_style="green"))
            else:
                self.console.print("[dim]You are empty-handed.[/dim]")
        else:
            if items:
                print("\nYou are carrying:")
                for item in items:
                    print(f"  - {item}")
            else:
                print("You are empty-handed.")
    
    def print_prompt(self) -> None:
        """Print command prompt."""
        if RICH_AVAILABLE and self.console:
            self.console.print("\n[bold green]>[/bold green] ", end="")
        else:
            print("\n> ", end="")
    
    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        if RICH_AVAILABLE and self.console:
            self.console.clear()
        else:
            print("\033[2J\033[H", end="")
    
    def print_banner(self) -> None:
        """Print ASCII art banner."""
        banner = """
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ███████╗████████╗██████╗  █████╗ ███╗   ██╗██████╗ ███████╗██████╗  ║
║   ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔══██╗██╔════╝██╔══██╗ ║
║   ███████╗   ██║   ██████╔╝███████║██╔██╗ ██║██║  ██║█████╗  ██║  ██║ ║
║   ╚════██║   ██║   ██╔══██╗██╔══██║██║╚██╗██║██║  ██║██╔══╝  ██║  ██║ ║
║   ███████║   ██║   ██║  ██║██║  ██║██║ ╚████║██████╔╝███████╗██████╔╝ ║
║   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═════╝  ║
║                                                                       ║
║        █████╗     ██████╗██╗  ██╗ ██████╗ ██████╗ ██╗   ██╗            ║
║       ██╔══██╗   ██╔════╝██║  ██║██╔═══██╗██╔══██╗╚██╗ ██╔╝            ║
║       ███████║   ██║     ███████║██║   ██║██████╔╝ ╚████╔╝             ║
║       ██╔══██║   ██║     ██╔══██║██║   ██║██╔══██╗  ╚██╔╝              ║
║       ██║  ██║   ╚██████╗██║  ██║╚██████╔╝██║  ██║   ██║               ║
║       ╚═╝  ╚═╝    ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝               ║
║                                                                       ║
║            Based on the novel by Ray Bradbury                          ║
║            Written by Len Neufeld and Byron Preiss                    ║
║                     Telarium 1984                                      ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
"""
        if RICH_AVAILABLE and self.console:
            self.console.print(banner, style="bold cyan")
        else:
            print(banner)
    
    def print_ending(self, ending_text: str, success: bool = False) -> None:
        """Print game ending."""
        if RICH_AVAILABLE and self.console:
            style = "bold green" if success else "bold red"
            self.console.print(Panel(ending_text, border_style=style))
        else:
            print(ending_text)
