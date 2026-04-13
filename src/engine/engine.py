"""Main game engine for Fahrenheit 451."""

from typing import Optional, List
from pathlib import Path
import json

from .parser import Parser, ParsedCommand
from .rooms import Room, RoomManager
from .inventory import Inventory, InventoryItem, create_default_items
from .state import GameState
from ..i18n import I18n, get_i18n


class GameEngine:
    """Main game engine for Fahrenheit 451."""
    
    def __init__(self):
        self.parser = Parser()
        self.room_manager = RoomManager()
        self.inventory = Inventory()
        self.state = GameState()
        self.default_items = create_default_items()
        self.command_history: List[str] = []
        self.message_buffer: List[str] = []
        self.i18n: I18n = get_i18n()
        self._room_map_es: dict = {}
        self._room_map_en: dict = {}
    
    def initialize(self, data_dir: Optional[Path] = None) -> None:
        """Initialize the game engine."""
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data"
        
        room_map_file = data_dir / "room_map.json"
        if room_map_file.exists():
            with open(room_map_file, 'r', encoding='utf-8') as f:
                self._room_map_en = json.load(f)
            for room_id, room_data in self._room_map_en.items():
                room = Room(
                    room_id=room_id,
                    name=room_data.get('name', room_id.replace('_', ' ').title()),
                    description=room_data.get('description', 'An empty space.'),
                    exits=room_data.get('exits', {})
                )
                self.room_manager.rooms[room_id] = room
        
        room_map_es_file = data_dir / "room_map_es.json"
        if room_map_es_file.exists():
            with open(room_map_es_file, 'r', encoding='utf-8') as f:
                self._room_map_es = json.load(f)
        
        objects_file = data_dir / "objects.json"
        if objects_file.exists():
            self.inventory.load_descriptions(objects_file)
        
        vocab_file = data_dir / "vocabulary.json"
        if vocab_file.exists():
            with open(vocab_file, 'r', encoding='utf-8') as f:
                vocab_data = json.load(f)
            words = vocab_data.get('vocabulary', {}).get('words', [])
            self.parser.load_vocabulary(words)
        
        for item_id, item in self.default_items.items():
            self.inventory.add(item)
    
    def set_language(self, lang: str) -> None:
        """Set the game language and reload rooms."""
        self.i18n.set_language(lang)
        self.parser.set_language(lang)
        
        if lang == 'es' and self._room_map_es:
            for room_id, room_data in self._room_map_es.items():
                room = Room(
                    room_id=room_id,
                    name=room_data.get('name', room_id.replace('_', ' ').title()),
                    description=room_data.get('description', 'Un espacio vacío.'),
                    exits=room_data.get('exits', {})
                )
                self.room_manager.rooms[room_id] = room
        elif self._room_map_en:
            for room_id, room_data in self._room_map_en.items():
                room = Room(
                    room_id=room_id,
                    name=room_data.get('name', room_id.replace('_', ' ').title()),
                    description=room_data.get('description', 'An empty space.'),
                    exits=room_data.get('exits', {})
                )
                self.room_manager.rooms[room_id] = room
    
    def start(self) -> None:
        """Start or restart the game."""
        self.state.reset()
        self.state.started = True
        self.state.current_room = 'opening'
        
        for item_id, item in self.default_items.items():
            self.inventory.add(item)
        
        self.message_buffer = []
        
        intro_title = self.i18n.get('intro.title')
        intro_text = self.i18n.get('intro.text')
        
        self.message_buffer.append(f"""
{'=' * 70}
{intro_title}
{'=' * 70}

{intro_text}
""")
        
        opening_text = self.i18n.get('opening.text')
        self.message_buffer.append(opening_text)
    
    def process_command(self, input_str: str) -> List[str]:
        """Process a player command and return output messages."""
        self.command_history.append(input_str)
        output = []
        
        parsed = self.parser.parse(input_str)
        
        if not parsed.verb:
            output.append(self.i18n.get('commands.unknown_command'))
            return output
        
        verb = parsed.verb.lower()
        
        if verb in ['look', 'l', 'mirar', 'm']:
            output.extend(self._do_look(parsed))
        elif verb in ['walk', 'go', 'caminar', 'ir']:
            output.extend(self._do_walk(parsed))
        elif verb in ['north', 'south', 'east', 'west', 'up', 'down',
                      'northeast', 'northwest', 'southeast', 'southwest',
                      'n', 's', 'e', 'w', 'u', 'd',
                      'norte', 'sur', 'este', 'oeste', 'arriba', 'abajo',
                      'noreste', 'noroeste', 'sureste', 'suroeste']:
            parsed.direction = verb
            output.extend(self._do_walk(parsed))
        elif verb in ['examine', 'inspect', 'x', 'examinar']:
            output.extend(self._do_examine(parsed))
        elif verb in ['inventory', 'inv', 'i', 'inventario']:
            output.extend(self._do_inventory())
        elif verb in ['take', 'get', 'tomar']:
            output.extend(self._do_take(parsed))
        elif verb in ['drop', 'discard', 'soltar', 'dejar']:
            output.extend(self._do_drop(parsed))
        elif verb in ['use', 'apply', 'usar']:
            output.extend(self._do_use(parsed))
        elif verb in ['speak', 'say', 'talk', 'hablar', 'decir']:
            output.extend(self._do_speak(parsed))
        elif verb in ['hint', 'help', '?', 'ayuda']:
            output.extend(self._do_hint())
        elif verb in ['quit', 'exit', 'q', 'salir']:
            output.append(self.i18n.get('ui.thanks_playing'))
            self.state.ended = True
        elif verb in ['restart', 'reiniciar']:
            self.start()
            return self.message_buffer
        elif verb in ['save', 'guardar']:
            self._do_save()
            output.append(self.i18n.get('commands.save_game', 'Game saved.'))
        elif verb in ['load', 'restore', 'cargar']:
            self._do_load()
            output.append(self.i18n.get('commands.load_game', 'Game loaded.'))
        else:
            output.append(self.i18n.get('commands.unknown_verb', 
                                       f"I don't know how to '{verb}'.").format(verb=verb))
            output.append(self.i18n.get('commands.try_commands'))
        
        self.message_buffer.extend(output)
        return output
    
    def _do_look(self, parsed: ParsedCommand) -> List[str]:
        """Handle LOOK command."""
        output = []
        
        if not parsed.noun1:
            room = self.room_manager.get_current_room(self.state)
            if room:
                if not room.visited:
                    output.append(room.description)
                    room.visited = True
                else:
                    output.append(room.description)
                
                if room.objects:
                    output.append(f"\n{self.i18n.get('commands.you_see', 'You can see:')} {', '.join(room.objects)}")
                
                output.append(f"\n{room.get_exits_string(self.i18n)}")
            return output
        
        output.extend(self._do_examine(parsed))
        return output
    
    def _do_walk(self, parsed: ParsedCommand) -> List[str]:
        """Handle GO/WALK command."""
        output = []
        
        direction = parsed.direction or parsed.noun1
        if not direction:
            output.append(self.i18n.get('commands.go_where'))
            return output
        
        direction = direction.lower()
        
        dir_map = {
            'n': 'north', 'north': 'north', 'norte': 'north',
            's': 'south', 'south': 'south', 'sur': 'south',
            'e': 'east', 'east': 'east', 'este': 'east',
            'w': 'west', 'west': 'west', 'oeste': 'west',
            'u': 'up', 'up': 'up', 'arriba': 'up',
            'd': 'down', 'down': 'down', 'abajo': 'down',
            'ne': 'northeast', 'northeast': 'northeast', 'noreste': 'northeast',
            'nw': 'northwest', 'northwest': 'northwest', 'noroeste': 'northwest',
            'se': 'southeast', 'southeast': 'southeast', 'sureste': 'southeast',
            'sw': 'southwest', 'southwest': 'southwest', 'suroeste': 'southwest'
        }
        
        direction = dir_map.get(direction, direction)
        
        room = self.room_manager.get_current_room(self.state)
        if not room:
            output.append("You're nowhere. This shouldn't happen.")
            return output
        
        next_room_id = room.get_exit(direction)
        if not next_room_id:
            dir_text = self.i18n.format_direction(direction)
            output.append(self.i18n.get('commands.cant_go', 
                                       f"You can't go {direction} from here.").format(direction=dir_text))
            output.append(room.get_exits_string(self.i18n))
            return output
        
        next_room = self.room_manager.get_room(next_room_id)
        if next_room:
            self.state.current_room = next_room_id
            output.append(f"\n{next_room.name.upper()}\n")
            output.append(next_room.description)
            next_room.visited = True
            
            if next_room.objects:
                output.append(f"\n{self.i18n.get('commands.you_see', 'You can see:')} {', '.join(next_room.objects)}")
            
            output.append(f"\n{next_room.get_exits_string(self.i18n)}")
        else:
            output.append(f"You walk {direction}...")
            output.append("(That area hasn't been mapped yet.)")
        
        return output
    
    def _do_examine(self, parsed: ParsedCommand) -> List[str]:
        """Handle EXAMINE command."""
        output = []
        
        if not parsed.noun1:
            output.append(self.i18n.get('commands.examine_what'))
            return output
        
        item = self.inventory.find_by_name(parsed.noun1)
        if item:
            output.append(item.description)
            return output
        
        desc = self.inventory.get_description(parsed.noun1)
        if desc:
            output.append(desc)
            return output
        
        room = self.room_manager.get_current_room(self.state)
        if room and parsed.noun1.lower() in [o.lower() for o in room.objects]:
            output.append(f"You examine the {parsed.noun1}.")
            return output
        
        output.append(self.i18n.get('commands.dont_see', 
                                   f"You don't see any '{parsed.noun1}' here.").format(item=parsed.noun1))
        return output
    
    def _do_inventory(self) -> List[str]:
        """Handle INVENTORY command."""
        output = []
        
        if self.inventory.is_empty():
            output.append(self.i18n.get('commands.empty_handed'))
        else:
            output.append(self.i18n.get('commands.carrying'))
            for item in self.inventory.items:
                output.append(f"  - {item.name}")
        
        return output
    
    def _do_take(self, parsed: ParsedCommand) -> List[str]:
        """Handle TAKE command."""
        output = []
        
        if not parsed.noun1:
            output.append(self.i18n.get('commands.take_what'))
            return output
        
        room = self.room_manager.get_current_room(self.state)
        if room and parsed.noun1.lower() in [o.lower() for o in room.objects]:
            room.remove_object(parsed.noun1)
            item = self.inventory.find_by_name(parsed.noun1)
            if item:
                output.append(self.i18n.get('commands.you_take', 
                                           f"You take the {item.name}.").format(item=item.name))
            else:
                new_item = InventoryItem(
                    parsed.noun1, parsed.noun1,
                    f"A {parsed.noun1}."
                )
                self.inventory.add(new_item)
                output.append(self.i18n.get('commands.you_take', 
                                           f"You take the {parsed.noun1}.").format(item=parsed.noun1))
        else:
            output.append(self.i18n.get('commands.dont_see', 
                                       f"You don't see any '{parsed.noun1}' here.").format(item=parsed.noun1))
        
        return output
    
    def _do_drop(self, parsed: ParsedCommand) -> List[str]:
        """Handle DROP command."""
        output = []
        
        if not parsed.noun1:
            output.append(self.i18n.get('commands.drop_what'))
            return output
        
        item = self.inventory.find_by_name(parsed.noun1)
        if item:
            room = self.room_manager.get_current_room(self.state)
            if room:
                room.add_object(item.item_id)
            self.inventory.remove(item.item_id)
            output.append(self.i18n.get('commands.you_drop', 
                                       f"You drop the {item.name}.").format(item=item.name))
        else:
            output.append(self.i18n.get('commands.not_carrying', 
                                       f"You aren't carrying any '{parsed.noun1}'.").format(item=parsed.noun1))
        
        return output
    
    def _do_use(self, parsed: ParsedCommand) -> List[str]:
        """Handle USE command."""
        output = []
        
        if not parsed.noun1:
            output.append(self.i18n.get('commands.use_what'))
            return output
        
        item = self.inventory.find_by_name(parsed.noun1)
        if item:
            output.append(self.i18n.get('commands.consider_using', 
                                       f"You consider using the {item.name}.").format(item=item.name))
            output.append(self.i18n.get('commands.not_implemented'))
        else:
            output.append(self.i18n.get('commands.dont_see', 
                                       f"You don't see any '{parsed.noun1}' here.").format(item=parsed.noun1))
        
        return output
    
    def _do_speak(self, parsed: ParsedCommand) -> List[str]:
        """Handle SPEAK/SAY command."""
        output = []
        
        if parsed.noun1:
            output.append(self.i18n.get('commands.say_something', 
                                       f"You say '{parsed.noun1}'.").format(words=parsed.noun1))
            output.append(self.i18n.get('commands.dialogue_not_impl'))
        else:
            output.append(self.i18n.get('commands.say_what'))
            output.append('SAY \"text\"')
        
        return output
    
    def _do_hint(self) -> List[str]:
        """Handle HELP/HINT command."""
        return [
            f"\n=== {self.i18n.get('help.title')} ===",
            f"\n{self.i18n.get('help.commands_title')}",
            f"  {self.i18n.get('help.look_cmd')}",
            f"  {self.i18n.get('help.go_cmd')}",
            f"  {self.i18n.get('help.move_cmd')}",
            f"  {self.i18n.get('help.examine_cmd')}",
            f"  {self.i18n.get('help.take_cmd')}",
            f"  {self.i18n.get('help.drop_cmd')}",
            f"  {self.i18n.get('help.inventory_cmd')}",
            f"  {self.i18n.get('help.say_cmd')}",
            f"  {self.i18n.get('help.use_cmd')}",
            f"  {self.i18n.get('help.save_cmd')}",
            f"  {self.i18n.get('help.load_cmd')}",
            f"  {self.i18n.get('help.restart_cmd')}",
            f"  {self.i18n.get('help.quit_cmd')}",
            f"\n{self.i18n.get('help.tips_title')}",
            f"  {self.i18n.get('help.tip1')}",
            f"  {self.i18n.get('help.tip2')}",
            f"  {self.i18n.get('help.tip3')}",
            f"  {self.i18n.get('help.tip4')}",
            "\n" + "=" * 50 + "\n"
        ]
    
    def _do_save(self) -> None:
        """Save the game."""
        self.state.save(Path("fahrenheit_451_save.json"))
    
    def _do_load(self) -> None:
        """Load a saved game."""
        self.state.load(Path("fahrenheit_451_save.json"))
    
    def is_game_over(self) -> bool:
        """Check if the game has ended."""
        return self.state.ended
    
    def get_current_room_name(self) -> str:
        """Get the name of the current room."""
        room = self.room_manager.get_current_room(self.state)
        return room.name if room else "Unknown"
    
    def get_room_description(self) -> str:
        """Get the description of the current room."""
        room = self.room_manager.get_current_room(self.state)
        return room.description if room else ""
