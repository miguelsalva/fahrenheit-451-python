#!/usr/bin/env python3
"""Extract object descriptions from Fahrenheit 451."""

import os
import json
from pathlib import Path

GAME_DIR = Path("/Users/miguel/Downloads/fahrenheit-451")

def extract_objects() -> dict:
    """Parse OBJ_DSCP and other object-related files."""
    filepath = GAME_DIR / "OBJ_DSCP"
    with open(filepath, 'rb') as f:
        data = f.read()
    
    result = {
        'header': data[:16].hex(),
        'objects': []
    }
    
    if data[:4] == b'S\x0a\xe7N':
        strings = []
        current = 0x10
        while current < len(data):
            end = data.find(b'\x00', current)
            if end == -1:
                break
            text = data[current:end].decode('latin-1', errors='replace')
            if text.strip():
                strings.append(text)
            current = end + 1
        
        result['objects'] = strings
    
    return result

def extract_memory() -> dict:
    """Parse MEMORY file with character memories/dialogues."""
    filepath = GAME_DIR / "MEMORY"
    with open(filepath, 'rb') as f:
        data = f.read()
    
    result = {
        'header': data[:16].hex() if len(data) >= 16 else '',
        'memories': []
    }
    
    if data[:4] == b'S\x0a\xe7N':
        strings = []
        current = 0x10
        while current < len(data):
            end = data.find(b'\x00', current)
            if end == -1:
                break
            text = data[current:end].decode('latin-1', errors='replace')
            if text.strip():
                strings.append(text)
            current = end + 1
        
        result['memories'] = strings
    
    return result

def main():
    print("Extracting objects from Fahrenheit 451...")
    
    objects = extract_objects()
    memories = extract_memory()
    
    output = {
        'objects': objects,
        'memories': memories
    }
    
    output_file = Path("/Users/miguel/Downloads/fahrenheit-451-new/src/data/objects.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(objects['objects'])} object descriptions")
    print(f"Extracted {len(memories['memories'])} memory entries")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()
