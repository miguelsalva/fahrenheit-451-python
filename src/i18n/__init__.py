"""Internationalization module for Fahrenheit 451."""

import json
from pathlib import Path
from typing import Optional, Dict, Any


class I18n:
    """Internationalization handler."""
    
    _instance: Optional['I18n'] = None
    _current_lang: str = 'en'
    _translations: Dict[str, Dict[str, Any]] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._translations:
            self._load_translations()
    
    def _load_translations(self) -> None:
        """Load all translation files."""
        i18n_dir = Path(__file__).parent
        for lang_file in i18n_dir.glob('*.json'):
            lang_code = lang_file.stem
            with open(lang_file, 'r', encoding='utf-8') as f:
                self._translations[lang_code] = json.load(f)
    
    def set_language(self, lang: str) -> None:
        """Set the current language."""
        if lang in self._translations:
            self._current_lang = lang
    
    def get_language(self) -> str:
        """Get the current language code."""
        return self._current_lang
    
    def get(self, key: str, default: Optional[str] = None) -> str:
        """Get a translation by key (dot notation supported)."""
        keys = key.split('.')
        result = self._translations.get(self._current_lang, {})
        
        for k in keys:
            if isinstance(result, dict):
                result = result.get(k, '')
            else:
                break
        
        if result == '' and default:
            return default
        
        if isinstance(result, dict):
            return str(result) if result else default or ''
        
        return str(result) if result else default or key
    
    def get_with_params(self, key: str, **params) -> str:
        """Get a translation with parameter substitution."""
        text = self.get(key)
        for param, value in params.items():
            text = text.replace(f'{{{param}}}', str(value))
        return text
    
    def format_direction(self, direction: str) -> str:
        """Format a direction name in current language."""
        dir_key = f'directions.{direction}'
        return self.get(dir_key, direction)
    
    def format_exit_string(self, exits: Dict[str, str]) -> str:
        """Format exits string in current language."""
        if not exits:
            return self.get('commands.no_exits')
        
        dir_list = []
        for direction in exits.keys():
            if exits[direction]:
                dir_list.append(self.format_direction(direction).upper())
        
        if not dir_list:
            return self.get('commands.no_exits')
        
        directions_str = ', '.join(dir_list)
        return self.get_with_params('commands.exits', directions=directions_str)


def get_i18n() -> I18n:
    """Get the global i18n instance."""
    return I18n()


def set_language(lang: str) -> None:
    """Set the global language."""
    get_i18n().set_language(lang)


def t(key: str, default: Optional[str] = None) -> str:
    """Shorthand for getting a translation."""
    return get_i18n().get(key, default)


def t_with_params(key: str, **params) -> str:
    """Shorthand for getting a translation with parameters."""
    return get_i18n().get_with_params(key, **params)
