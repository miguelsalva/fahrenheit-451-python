"""Inventory management for Fahrenheit 451."""

from typing import Dict, List, Optional
import json
from pathlib import Path


class InventoryItem:
    """Represents an item in the player's inventory."""
    
    def __init__(
        self,
        item_id: str,
        name: str,
        description: str,
        can_take: bool = True,
        weight: int = 0,
        properties: Optional[Dict] = None
    ):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.can_take = can_take
        self.weight = weight
        self.properties = properties or {}
    
    def to_dict(self) -> Dict:
        """Convert item to dictionary."""
        return {
            'item_id': self.item_id,
            'name': self.name,
            'description': self.description,
            'can_take': self.can_take,
            'weight': self.weight,
            'properties': self.properties
        }


class Inventory:
    """Manages the player's inventory."""
    
    MAX_WEIGHT = 50
    
    def __init__(self):
        self.items: List[InventoryItem] = []
        self.item_dict: Dict[str, InventoryItem] = {}
        self.descriptions: Dict[str, str] = {}
    
    def load_descriptions(self, filepath: Path) -> None:
        """Load object descriptions from JSON."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        objects = data.get('objects', {}).get('objects', [])
        for i, desc in enumerate(objects):
            self.descriptions[f"obj_{i}"] = desc
    
    def add(self, item: InventoryItem) -> bool:
        """Add an item to inventory."""
        if item.item_id in self.item_dict:
            return False
        
        total_weight = sum(it.weight for it in self.items)
        if total_weight + item.weight > self.MAX_WEIGHT:
            return False
        
        self.items.append(item)
        self.item_dict[item.item_id] = item
        return True
    
    def remove(self, item_id: str) -> Optional[InventoryItem]:
        """Remove an item from inventory."""
        if item_id not in self.item_dict:
            return None
        
        item = self.item_dict.pop(item_id)
        self.items.remove(item)
        return item
    
    def get(self, item_id: str) -> Optional[InventoryItem]:
        """Get an item by ID."""
        return self.item_dict.get(item_id)
    
    def has(self, item_id: str) -> bool:
        """Check if inventory has an item."""
        return item_id in self.item_dict
    
    def find_by_name(self, name: str) -> Optional[InventoryItem]:
        """Find an item by name (partial match)."""
        name_lower = name.lower()
        for item in self.items:
            if name_lower in item.name.lower() or name_lower in item.item_id.lower():
                return item
        return None
    
    def list_items(self) -> List[str]:
        """List all items in inventory."""
        return [item.name for item in self.items]
    
    def is_empty(self) -> bool:
        """Check if inventory is empty."""
        return len(self.items) == 0
    
    def get_weight(self) -> int:
        """Get total weight of inventory."""
        return sum(item.weight for item in self.items)
    
    def get_description(self, item_id: str) -> Optional[str]:
        """Get description for an item."""
        return self.descriptions.get(item_id)
    
    def to_list(self) -> List[Dict]:
        """Convert inventory to list of dicts."""
        return [item.to_dict() for item in self.items]


def create_default_items() -> Dict[str, InventoryItem]:
    """Create the default inventory items for the game."""
    return {
        'glasses': InventoryItem(
            'glasses',
            'thick-lensed glasses',
            'The glasses are thick-lensed and horn-rimmed.',
            can_take=True,
            weight=1
        ),
        'jacket': InventoryItem(
            'jacket',
            'plaid jacket',
            'The jacket is plaid and pile lined.',
            can_take=True,
            weight=2
        ),
        'permit': InventoryItem(
            'permit',
            'firefighter permit',
            'The permit is an entry permit to the library.',
            can_take=True,
            weight=1
        ),
        'id': InventoryItem(
            'id',
            'identification card',
            'The id is a plastic covered card with a picture on it.',
            can_take=True,
            weight=1
        ),
        'lasergun': InventoryItem(
            'lasergun',
            'laser gun',
            'A standard issue firefighting weapon.',
            can_take=True,
            weight=3
        ),
        'lighter': InventoryItem(
            'lighter',
            'cigarette lighter',
            'A silver cigarette lighter.',
            can_take=True,
            weight=1
        ),
        'rifle': InventoryItem(
            'rifle',
            'hunting rifle',
            'An old but well-maintained hunting rifle.',
            can_take=True,
            weight=5
        ),
        'money': InventoryItem(
            'money',
            'money',
            'The money is a mixture of crisp new bills.',
            can_take=True,
            weight=1
        ),
        'card': InventoryItem(
            'card',
            'white plastic card',
            'The card is made of white plastic card.',
            can_take=True,
            weight=1
        ),
        'bank_card': InventoryItem(
            'bank-card',
            'bank card',
            'The bank-card is made of plastic.',
            can_take=True,
            weight=1
        ),
        'phone': InventoryItem(
            'phone',
            'phone number',
            'A phone number written on a piece of paper.',
            can_take=True,
            weight=1
        )
    }
