#!/usr/bin/env python3
"""Fahrenheit 451 - Terminal Text Adventure Game.

A recreation of the classic text adventure game for modern terminals.
Supports English and Spanish.
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.engine import GameEngine
from src.ui import TerminalUI
from src.i18n import set_language, get_i18n


def print_language_menu() -> str:
    """Print language selection menu and return selected language."""
    print("""
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
""")
    
    print("Select Language / Seleccionar Idioma:")
    print("  [1] English")
    print("  [2] Español")
    print()
    
    while True:
        try:
            choice = input("Choice / Elección: ").strip()
            if choice == '1':
                return 'en'
            elif choice == '2':
                return 'es'
            else:
                print("Please enter 1 or 2 / Por favor, introduce 1 o 2")
        except (EOFError, KeyboardInterrupt):
            print("\nDefaulting to English...")
            return 'en'


def main():
    """Main entry point for the game."""
    ui = TerminalUI()
    
    ui.clear_screen()
    
    lang = print_language_menu()
    set_language(lang)
    
    print("\n" + "=" * 70)
    if lang == 'es':
        print("¡Bienvenido a Fahrenheit 451 - Edición Terminal!")
    else:
        print("Welcome to Fahrenheit 451 - Terminal Edition!")
    print("=" * 70)
    
    if lang == 'es':
        print("\nPulsa ENTER para comenzar tu aventura...")
    else:
        print("\nPress ENTER to start your adventure...")
    input()
    
    engine = GameEngine()
    
    data_dir = Path(__file__).parent.parent / "src" / "data"
    if not data_dir.exists():
        print(f"Error: Data directory not found: {data_dir}")
        print("Please ensure the data files are in place.")
        sys.exit(1)
    
    engine.initialize(data_dir)
    engine.set_language(lang)
    engine.start()
    
    for message in engine.message_buffer:
        ui.print_message(message)
    
    print("\n" + "=" * 70)
    
    thanks_msg = get_i18n().get('ui.thanks_playing')
    memory_msg = get_i18n().get('ui.memory_forever')
    
    while not engine.is_game_over():
        ui.print_prompt()
        try:
            command = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            print(thanks_msg)
            print(memory_msg)
            break
        
        if not command:
            continue
        
        outputs = engine.process_command(command)
        
        for line in outputs:
            if line.strip():
                print(line)
        
        print()
    
    print("\n" + "=" * 70)
    print(thanks_msg)
    print(memory_msg)
    print("=" * 70)


if __name__ == "__main__":
    main()
