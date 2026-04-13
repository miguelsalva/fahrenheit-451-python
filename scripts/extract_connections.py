#!/usr/bin/env python3
"""Analyze room files to extract exits/connections."""

import re
from pathlib import Path
import json

GAME_DIR = Path("/Users/miguel/Downloads/fahrenheit-451")

DIRECTION_PATTERNS = [
    ('north', r'\b(north|n|s)\b'),
    ('south', r'\b(south|s)\b'),
    ('east', r'\b(east|e)\b'),
    ('west', r'\b(west|w)\b'),
    ('up', r'\b(up|u)\b'),
    ('down', r'\b(down|d)\b'),
]

def extract_room_connections(room_name: str, filepath: Path) -> dict:
    """Extract directional connections from room description."""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    text = data[data.find(b'\x00')+1:].decode('latin-1', errors='replace')
    text = text.lower()
    
    connections = {}
    
    text_lower = text.lower()
    
    if 'runs north' in text_lower or 'leads north' in text_lower or 'go north' in text_lower:
        connections['north'] = None
    if 'runs south' in text_lower or 'leads south' in text_lower or 'go south' in text_lower:
        connections['south'] = None
    if 'runs east' in text_lower or 'leads east' in text_lower or 'go east' in text_lower:
        connections['east'] = None
    if 'runs west' in text_lower or 'leads west' in text_lower or 'go west' in text_lower:
        connections['west'] = None
    if 'runs up' in text_lower or 'leads up' in text_lower or 'go up' in text_lower:
        connections['up'] = None
    if 'runs down' in text_lower or 'leads down' in text_lower or 'go down' in text_lower:
        connections['down'] = None
    if 'southwest' in text_lower:
        connections['southwest'] = None
    if 'southeast' in text_lower:
        connections['southeast'] = None
    if 'northwest' in text_lower:
        connections['northwest'] = None
    if 'northeast' in text_lower:
        connections['northeast'] = None
    
    return connections

def main():
    print("Analyzing room connections...")
    
    room_files = [
        "APARTMEN", "OPENING", "QUESTION", "HOSPITAL", "PLAZA_HO",
        "FOUNTAIN", "BANK", "FOOD_CEN", "TOWER", "TREATMEN",
        "HEADQUAR", "BOOKSTOR", "DEN_OF_T", "DETENTIO", "WALKWAY",
        "LIB_ENTR", "LIB_STEP", "LIB_FIRS", "LIB_SECO", "LIB_RM_1",
        "LIB_RM_2", "LIB_ROOF", "LIB_GUAR", "SUBWAY_S", "SUBWAY_C",
        "BASEMENT", "LOUNGE", "STATION_", "PHANTASY", "CATHEDRA",
        "POWER_CE", "OFFICE_B", "UNDERGRO", "RADIATIO", "HOUNDS_B",
        "IN_HOUND", "HOUND_PA", "PATROL_4", "HOSPITAL", "THINK_TA",
        "ENGRAVER", "JEWELRY_", "GLASS_WO", "MAGIC_SH", "WALLS_PA",
        "CLOSED_C", "CLOSED_B", "CLOSED_T", "PHONE_BO", "PHONE_ME",
        "OBSERVAT", "SECOND_F", "FORTY_TH", "CELL_BLO", "RESTAURA",
        "FIFTH_AV", "EIGHTH_F", "PARK", "TUNNEL", "SMALL_PL",
        "POST_451"
    ]
    
    connections = {}
    for room_file in room_files:
        filepath = GAME_DIR / room_file
        if filepath.exists():
            room_id = room_file.lower().rstrip('_')
            conns = extract_room_connections(room_id, filepath)
            if conns:
                connections[room_id] = conns
    
    output = {"connections": connections}
    
    output_file = Path("/Users/miguel/Downloads/fahrenheit-451-new/src/data/connections.json")
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Found connections for {len(connections)} rooms:")
    for room_id, conns in list(connections.items())[:10]:
        print(f"  {room_id}: {list(connections[room_id].keys())}")
    print(f"  ... and {len(connections)-10} more")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()
