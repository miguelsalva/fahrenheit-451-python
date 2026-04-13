"""Parser for Fahrenheit 451 text commands."""

import re
from typing import Optional, List, Dict
from dataclasses import dataclass


@dataclass
class ParsedCommand:
    """Represents a parsed player command."""
    verb: Optional[str] = None
    noun1: Optional[str] = None
    noun2: Optional[str] = None
    preposition: Optional[str] = None
    original: str = ""
    is_direction: bool = False
    direction: Optional[str] = None


class Parser:
    """Text parser for the Fahrenheit 451 adventure game."""
    
    DIRECTION_WORDS = {
        'n': 'north', 'north': 'north',
        's': 'south', 'south': 'south',
        'e': 'east', 'east': 'east',
        'w': 'west', 'west': 'west',
        'u': 'up', 'up': 'up',
        'd': 'down', 'down': 'down',
        'ne': 'northeast', 'northeast': 'northeast',
        'nw': 'northwest', 'northwest': 'northwest',
        'se': 'southeast', 'southeast': 'southeast',
        'sw': 'southwest', 'southwest': 'southwest',
        'norte': 'north', 'sur': 'south', 'este': 'east', 'oeste': 'west',
        'arriba': 'up', 'abajo': 'down',
        'noreste': 'northeast', 'noroeste': 'northwest',
        'sureste': 'southeast', 'suroeste': 'southwest'
    }
    
    VERB_ALIASES = {
        'go': 'walk', 'move': 'walk', 'run': 'walk',
        'get': 'take', 'grab': 'take', 'pick': 'take',
        'inspect': 'examine', 'check': 'examine', 'read': 'examine', 'x': 'examine',
        'look': 'look', 'l': 'look', 'mirar': 'look', 'm': 'look',
        'i': 'inventory', 'inv': 'inventory', 'inventario': 'inventory',
        'quit': 'exit', 'q': 'exit', 'salir': 'exit',
        'say': 'speak', 'talk': 'speak', 'hablar': 'speak', 'decir': 'speak',
        'use': 'use', 'usar': 'use',
        'drop': 'drop', 'leave': 'drop', 'soltar': 'drop', 'dejar': 'drop',
        'take': 'take', 'tomar': 'take',
        'open': 'unlock', 'close': 'shut',
        'help': 'help', '?': 'help', 'ayuda': 'help',
        'save': 'save', 'guardar': 'save',
        'load': 'load', 'restore': 'load', 'cargar': 'load',
        'restart': 'restart', 'reiniciar': 'restart'
    }
    
    PREPOSITIONS = {
        'to', 'with', 'on', 'at', 'in', 'from', 'into',
        'through', 'under', 'over', 'across',
        'a', 'con', 'en', 'de', 'desde', 'hacia', 'por'
    }
    
    def __init__(self):
        self.vocabulary: set[str] = set()
        self.verbs: set[str] = set()
        self.nouns: set[str] = set()
        self.current_lang: str = 'en'
    
    def set_language(self, lang: str) -> None:
        """Set the parser language."""
        self.current_lang = lang
    
    def load_vocabulary(self, words: list[str]) -> None:
        """Load vocabulary from extracted data."""
        self.vocabulary = {w.lower() for w in words}
        for word in words:
            w = word.lower()
            if w not in self.DIRECTION_WORDS:
                self.verbs.add(w)
    
    def parse(self, input_str: str) -> ParsedCommand:
        """Parse a player input string into a command structure."""
        result = ParsedCommand(original=input_str)
        
        if not input_str.strip():
            return result
        
        words = re.findall(r'[\w\'-]+', input_str.lower())
        if not words:
            return result
        
        cleaned = []
        for w in words:
            if w in self.VERB_ALIASES:
                cleaned.append(self.VERB_ALIASES[w])
            else:
                cleaned.append(w)
        
        if cleaned[0] in self.DIRECTION_WORDS:
            result.is_direction = True
            result.direction = self.DIRECTION_WORDS[cleaned[0]]
            result.verb = 'walk'
            return result
        
        result.verb = cleaned[0] if cleaned else None
        
        prepositions_found = []
        words_after_verb = []
        
        for i, word in enumerate(cleaned[1:], 1):
            if word in self.PREPOSITIONS:
                prepositions_found.append((i, word))
            else:
                words_after_verb.append(word)
        
        if words_after_verb:
            result.noun1 = words_after_verb[0]
        if len(words_after_verb) > 1:
            result.noun2 = words_after_verb[1]
        
        if prepositions_found and len(prepositions_found) > 0:
            result.preposition = prepositions_found[0][1]
        
        return result
    
    def expand_synonyms(self, word: str) -> list[str]:
        """Return a list of synonyms for word matching."""
        return [word]
