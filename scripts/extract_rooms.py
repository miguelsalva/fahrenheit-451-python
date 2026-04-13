#!/usr/bin/env python3
"""Extract room data from Fahrenheit 451 game files."""

import os
import json
from pathlib import Path

GAME_DIR = Path("/Users/miguel/Downloads/fahrenheit-451")

ROOM_FILES = [
    "LIB_ROOF", "HOSPITAL", "BANK", "ENGRAVER", "JEWELRY_", "FOOD_CEN",
    "TREATMEN", "HEADQUAR", "PHANTASY", "APARTMEN", "BOOKSTOR", "DEN_OF_T",
    "DETENTIO", "WALKWAY", "MAGIC_SH", "WALLS_PA", "GLASS_WO", "THINK_TA",
    "POWER_CE", "OFFICE_B", "UNDERGRO", "RADIATIO", "CLOSED_C", "CLOSED_B",
    "CLOSED_T", "PHONE_BO", "PHONE_ME", "OBSERVAT", "SECOND_F", "FORTY_TH",
    "CELL_BLO", "LIB_SECO", "LIB_RM_2", "LIB_ROOF", "LIB_FIRS", "LIB_RM_1",
    "HOUND_PA", "LIB_GUAR", "IN_HOUND", "HOUNDS_B", "PATROL_4", "STATION_",
    "SUBWAY_C", "SUBWAY_S", "BASEMENT", "FOUNTAIN", "PLAZA_HO", "TOWER",
    "PARK", "TUNNEL", "SMALL_PL", "LOUNGE", "EIGHTH_F", "PHANTASY",
    "FIFTH_AV", "LIBRARY", "CATHEDRA", "RESTAURA", "LIB_STEP", "POST_451"
]

def extract_text_from_bytes(data: bytes, start: int) -> list[str]:
    """Extract null-terminated strings from binary data."""
    strings = []
    current = start
    while current < len(data):
        end = data.find(b'\x00', current)
        if end == -1:
            break
        text = data[current:end].decode('latin-1', errors='replace')
        if text.strip():
            strings.append(text)
        current = end + 1
    return strings

def parse_room_file(filepath: Path) -> dict:
    """Parse a room file and extract its contents."""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    result = {
        'filename': filepath.name,
        'descriptions': [],
        'header': data[:16].hex() if len(data) >= 16 else ''
    }
    
    if data[:4] == b'S\x0a\xe7N':
        strings = extract_text_from_bytes(data, 0x50)
        result['descriptions'] = strings
    
    return result

def parse_dir_file() -> dict:
    """Parse the DIR file which contains room mappings."""
    filepath = GAME_DIR / "DIR"
    with open(filepath, 'rb') as f:
        content = f.read().decode('latin-1', errors='replace')
    
    rooms = {}
    for line in content.split('\r\n'):
        if ':' in line and line.strip():
            prefix, room_id = line.split(':', 1)
            rooms[room_id.strip()] = {'prefix': prefix.strip()}
    
    return rooms

def main():
    print("Extracting room data from Fahrenheit 451...")
    
    rooms_dir = {}
    for room_file in ROOM_FILES:
        filepath = GAME_DIR / room_file
        if filepath.exists():
            room_data = parse_room_file(filepath)
            room_id = room_file.lower().rstrip('_')
            rooms_dir[room_id] = room_data
    
    output = {
        'rooms': rooms_dir,
        'room_index': parse_dir_file()
    }
    
    output_file = Path("/Users/miguel/Downloads/fahrenheit-451-new/src/data/rooms.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(rooms_dir)} rooms to {output_file}")

if __name__ == "__main__":
    main()
