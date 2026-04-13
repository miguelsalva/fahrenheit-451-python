"""Room management for Fahrenheit 451."""

from typing import Dict, List, Optional, Any
import json
from pathlib import Path


class Room:
    """Represents a room/location in the game."""
    
    def __init__(
        self,
        room_id: str,
        name: str,
        description: str,
        short_description: Optional[str] = None,
        exits: Optional[Dict[str, str]] = None,
        objects: Optional[List[str]] = None,
        conditions: Optional[Dict[str, Any]] = None,
        visited: bool = False
    ):
        self.room_id = room_id
        self.name = name
        self.description = description
        self.short_description = short_description or description[:100] + "..."
        self.exits = exits or {}
        self.objects = objects or []
        self.conditions = conditions or {}
        self.visited = visited
    
    def has_exit(self, direction: str) -> bool:
        """Check if room has an exit in given direction."""
        return direction.lower() in self.exits
    
    def get_exit(self, direction: str) -> Optional[str]:
        """Get the room ID for an exit in given direction."""
        return self.exits.get(direction.lower())
    
    def add_object(self, obj_id: str) -> None:
        """Add an object to the room."""
        if obj_id not in self.objects:
            self.objects.append(obj_id)
    
    def remove_object(self, obj_id: str) -> bool:
        """Remove an object from the room."""
        if obj_id in self.objects:
            self.objects.remove(obj_id)
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert room to dictionary."""
        return {
            'room_id': self.room_id,
            'name': self.name,
            'description': self.description,
            'short_description': self.short_description,
            'exits': self.exits,
            'objects': self.objects,
            'conditions': self.conditions,
            'visited': self.visited
        }
    
    def get_exits_string(self, i18n=None) -> str:
        """Get a formatted string of available exits."""
        if not self.exits:
            if i18n:
                return i18n.get('commands.no_exits')
            return "There are no obvious exits."
        
        directions = []
        for direction, dest in self.exits.items():
            if dest:
                if i18n:
                    directions.append(i18n.format_direction(direction).upper())
                else:
                    directions.append(direction.upper())
        
        if not directions:
            if i18n:
                return i18n.get('commands.no_exits')
            return "There are no obvious exits."
        
        if i18n:
            return i18n.get_with_params('commands.exits', directions=', '.join(directions))
        return f"Exits: {', '.join(directions)}"


class RoomManager:
    """Manages all rooms in the game."""
    
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.room_index: Dict[str, Dict[str, str]] = {}
    
    def load_from_json(self, filepath: Path) -> None:
        """Load rooms from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        rooms_data = data.get('rooms', {})
        for room_id, room_data in rooms_data.items():
            descriptions = room_data.get('descriptions', [])
            full_desc = '\n'.join(descriptions) if descriptions else "An empty space."
            
            room = Room(
                room_id=room_id,
                name=room_id.replace('_', ' ').title(),
                description=full_desc,
                short_description=descriptions[0] if descriptions else full_desc[:100]
            )
            self.rooms[room_id] = room
        
        self.room_index = data.get('room_index', {})
    
    def get_room(self, room_id: str) -> Optional[Room]:
        """Get a room by ID."""
        return self.rooms.get(room_id.lower())
    
    def get_current_room(self, state) -> Optional[Room]:
        """Get the current room from game state."""
        if state.current_room:
            return self.get_room(state.current_room)
        
        for room_id, room in self.rooms.items():
            return room
        return None
    
    def set_room_exits(self, room_id: str, exits: Dict[str, str]) -> None:
        """Set exits for a room."""
        room = self.get_room(room_id)
        if room:
            room.exits = exits
    
    def get_random_start_room(self) -> Optional[str]:
        """Get a random starting room for the game."""
        for room_id, room in self.rooms.items():
            if room_id in ['apartment', 'apartmen', 'opening', 'question']:
                return room_id
        return 'opening'
