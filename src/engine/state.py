"""Game state management for Fahrenheit 451."""

from typing import Dict, Any, Set
import json
from pathlib import Path


class GameState:
    """Manages the game state including flags, variables, and history."""
    
    def __init__(self):
        self.flags: Dict[str, int] = {}
        self.variables: Dict[str, Any] = {}
        self.history: list[str] = []
        self.turn_count: int = 0
        self.current_room: str = ""
        self.started: bool = False
        self.ended: bool = False
        self.ending_type: str = ""
    
    def set_flag(self, flag: str, value: int = 1) -> None:
        """Set a game flag."""
        self.flags[flag] = value
    
    def get_flag(self, flag: str, default: int = 0) -> int:
        """Get a game flag value."""
        return self.flags.get(flag, default)
    
    def increment_flag(self, flag: str, amount: int = 1) -> int:
        """Increment a flag and return new value."""
        self.flags[flag] = self.get_flag(flag) + amount
        return self.flags[flag]
    
    def set_variable(self, var: str, value: Any) -> None:
        """Set a game variable."""
        self.variables[var] = value
    
    def get_variable(self, var: str, default: Any = None) -> Any:
        """Get a game variable."""
        return self.variables.get(var, default)
    
    def add_to_history(self, action: str) -> None:
        """Add an action to command history."""
        self.history.append(action)
        if len(self.history) > 100:
            self.history = self.history[-100:]
    
    def increment_turn(self) -> None:
        """Increment the turn counter."""
        self.turn_count += 1
    
    def save(self, filepath: Path) -> bool:
        """Save game state to file."""
        try:
            save_data = {
                'flags': self.flags,
                'variables': self.variables,
                'history': self.history,
                'turn_count': self.turn_count,
                'current_room': self.current_room,
                'started': self.started,
                'ended': self.ended,
                'ending_type': self.ending_type
            }
            with open(filepath, 'w') as f:
                json.dump(save_data, f)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load(self, filepath: Path) -> bool:
        """Load game state from file."""
        try:
            with open(filepath, 'r') as f:
                save_data = json.load(f)
            self.flags = save_data.get('flags', {})
            self.variables = save_data.get('variables', {})
            self.history = save_data.get('history', [])
            self.turn_count = save_data.get('turn_count', 0)
            self.current_room = save_data.get('current_room', '')
            self.started = save_data.get('started', True)
            self.ended = save_data.get('ended', False)
            self.ending_type = save_data.get('ending_type', '')
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
    
    def reset(self) -> None:
        """Reset game state to initial values."""
        self.__init__()
