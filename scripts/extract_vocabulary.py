#!/usr/bin/env python3
"""Extract vocabulary from Fahrenheit 451 game files."""

import os
import json
from pathlib import Path

GAME_DIR = Path("/Users/miguel/Downloads/fahrenheit-451")

def extract_vocabulary() -> dict:
    """Parse the F451.V vocabulary file."""
    filepath = GAME_DIR / "F451.V"
    with open(filepath, 'rb') as f:
        data = f.read()
    
    result = {
        'header': data[:16].hex(),
        'words': [],
        'categories': {}
    }
    
    word_table_offset = int.from_bytes(data[4:6], 'little')
    num_words = int.from_bytes(data[6:8], 'little')
    
    print(f"Word table offset: 0x{word_table_offset:04x}")
    print(f"Number of words: {num_words}")
    
    i = 0x40
    word_num = 0
    while i < len(data) and word_num < 500:
        b = data[i]
        if 0x20 <= b <= 0x7e:
            word = ''
            j = i
            while j < len(data) and 0x20 <= data[j] <= 0x7e:
                word += chr(data[j])
                j += 1
            if word:
                result['words'].append(word)
            i = j + 1
            word_num += 1
        else:
            i += 1
    
    return result

def extract_dir_index() -> dict:
    """Parse the DIR file."""
    filepath = GAME_DIR / "DIR"
    with open(filepath, 'rb') as f:
        content = f.read().decode('latin-1', errors='replace')
    
    index = {}
    for line in content.split('\r\n'):
        if ':' in line and line.strip():
            prefix, room_id = line.split(':', 1)
            index[room_id.strip()] = {
                'prefix': prefix.strip(),
                'type': 'area' if prefix.strip() == 'a' else 'binary'
            }
    
    return index

def main():
    print("Extracting vocabulary from Fahrenheit 451...")
    
    vocab = extract_vocabulary()
    dir_index = extract_dir_index()
    
    output = {
        'vocabulary': vocab,
        'room_index': dir_index
    }
    
    output_file = Path("/Users/miguel/Downloads/fahrenheit-451-new/src/data/vocabulary.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(vocab['words'])} vocabulary words")
    print(f"Room index has {len(dir_index)} entries")
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()
