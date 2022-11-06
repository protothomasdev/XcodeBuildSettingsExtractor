"""This module provides the settings model."""

class Setting:
    """A class that represents an Xcode build setting."""

    # Types a setting can have
    TYPE_STRING = 'String'
    TYPE_STRINGLIST = 'StringList'
    TYPE_PATH = 'Path'
    TYPE_PATHLIST = 'PathList'
    TYPE_BOOLEAN = 'Boolean'
    TYPE_ENUM = 'Enumeration'
    
    def __init__(self, name:str, description:str, key:str, type:str, category:str, default_value, enum_cases):
        self.name = name
        self.description = description
        self.key = key
        self.type = self._mapped_type(type)
        self.category = category
        self.default_value = default_value
        self.enum_cases = enum_cases

        # if for some reason the default value is not in the list of values, add it.
        if self.default_value != None and self.default_value not in self.enum_cases:
            # do not add it if the default value is a variable
            if not self.default_value.startswith('$('):
                self.enum_cases.append(self.default_value)

    def __repr__(self):
        return f"<{self.name}>"

    def __eq__(self, other) -> bool:
        # settings with the same key are considered equal
        return self.key == other.key

    def __hash__(self) -> int:
        # settings with the same key are considered equal
        return hash(('key', self.key))

    def _mapped_type(self, type: str) -> str:
        if type == 'string':
            return self.TYPE_STRING
        elif type == 'stringlist':
            return self.TYPE_STRINGLIST
        if type == 'path':
            return self.TYPE_STRING
        elif type == 'pathlist':
            return self.TYPE_STRINGLIST
        elif type == 'bool':
            return self.TYPE_BOOLEAN
        elif type == 'Bool':
            return self.TYPE_BOOLEAN
        elif type == 'enum':
            return self.TYPE_ENUM
        elif type == 'CodeSignIdentity':
            return self.TYPE_STRING
        elif type == 'OpenCLArchitectures':
            return self.TYPE_STRING
        elif type == 'CodeSignStyle':
            return self.TYPE_ENUM
        elif type == 'DevelopmentTeam':
            return self.TYPE_STRING
        elif type == 'ProvisioningProfileSpecifier':
            return self.TYPE_STRING
        elif type == 'CompilerVersion':
            return self.TYPE_STRING
        elif type == 'ProvisioningProfile':
            return self.TYPE_STRING
        return type