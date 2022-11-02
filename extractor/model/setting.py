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

        # if for some reason the default value is not in the list of values, add it.
        if self.default_value != None and self.default_value not in self.values:
            # do not add it if the default value is a variable
            if not self.default_value.startswith('$('):
                self.values.append(self.default_value)

    def __repr__(self):
        return f"<{self.name}>"

    def __eq__(self, other) -> bool:
        # settings with the same key are considered equal
        return self.key == other.key

    def __hash__(self) -> int:
        # settings with the same key are considered equal
        return hash(('key', self.key))