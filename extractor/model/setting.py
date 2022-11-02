"""This module provides the settings model."""

class Setting:
    """A class that represents an Xcode build setting."""
    
    def __init__(self, name:str, description:str, key:str, type:str, category:str, default_value, values):
        self.name = name
        self.description = description
        self.key = key
        self.type = type
        self.category = category
        self.default_value = default_value
        self.values = values

    def __repr__(self):
        return f"<{self.name}>"

    def __eq__(self, other) -> bool:
        # settings with the same key are considered equal
        return self.key == other.key

    def __hash__(self) -> int:
        # settings with the same key are considered equal
        return hash(('key', self.key))