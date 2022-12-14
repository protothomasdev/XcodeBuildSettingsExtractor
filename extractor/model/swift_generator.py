"""This module provides methods to generate Swift code from settings."""
from re import sub
from typing import Optional
from .setting import Setting

_TAB = '    '
_EMPTY_LINE = '\n'

def to_swift_code(s: Setting) -> str:
    """Generates swift code from a given setting."""
    string = ''
    if s.type == "Enumeration":
        string += _enum(s)
        string += _EMPTY_LINE
    
    string += _func(s)
    string += _EMPTY_LINE

    return string

def _func(s: Setting) -> str:
    string = ''
    if s.description != None:
        for line in s.description.split('\n'):
            string += _TAB +_documentation(line) + '\n'
    
    string += _TAB + _func_name(s)
    string += ' {\n'
    string += _TAB + _TAB + 'var newDict = self' + '\n'
    string += _TAB + _TAB + f'newDict[\"{s.key}\"] = {_save_value_statement(s)}' + '\n'
    string += _TAB + _TAB + 'return newDict' + '\n'
    string += _TAB + '}'
    return string

def _enum(s: Setting) -> str:
    if s.enum_cases == None:
        return ''
    string = ''
    string += _TAB + f'enum {_enum_name(s.key)}: String' + ' {\n'

    for v in s.enum_cases:
        string += _TAB + _TAB + f'case {_enum_case_name(v)} = \"{v}\"' + '\n'

    string += _TAB + '}\n'
    return string

def _enum_name(name: str) -> str:
    string = _camel_case(name, start_lower=False)
    return string + 'Value'

def _enum_case_name(name: str) -> str:
    if len(name) == 0:
        return 'empty'
    elif name.lower() == 'default':
        return 'Default'
    elif name == 'extension':
        return 'Extension'
    elif name == 'XML':
        return 'XML'
    elif name == 'Binary':
        return 'Binary'
    elif name == 'UIStatusBarStyleDefault':
        return 'Default'
    elif name.startswith("UIStatusBarStyle"):
        s = name[len("UIStatusBarStyle"):]
        return ''.join([s[0].lower(), s[1:]])
    elif name[0].isdigit():
        return f'_{name}'
    return _camel_case(name)

def _camel_case(text: str, start_lower: bool = True) -> str:
    # replace special characters with whitespace, uppercase the first letter of every word, remove whitespace
    s = sub(r"(_|-|\.|\+)+", " ", text).title().replace(" ", "")
    if start_lower:
        if len(s) == 1:
            return s[0].lower()
        else:
            return ''.join([s[0].lower(), s[1:]])
    else:
        if len(s) == 1:
            return s[0].upper()
        else:
            return ''.join([s[0].upper(), s[1:]])

def _documentation(text: str) -> str:
    return '/// ' + text

def _func_name(s: Setting):
    name = 'func ' + _camel_case(s.key)
    name += '('
    if s.type == Setting.TYPE_STRING:
        name += '_ value: String'
    elif s.type == Setting.TYPE_STRINGLIST:
        name += '_ values: [String]'
    elif s.type == Setting.TYPE_PATH:
        name += '_ path: Path'
    elif s.type == Setting.TYPE_PATHLIST:
        name += '_ paths: [Path]'
    elif s.type == Setting.TYPE_BOOLEAN:
        name += '_ bool: Bool'
    elif s.type == Setting.TYPE_ENUM:
        name += f'_ value: {_enum_name(s.key)}'

    default = _default_value(s)
    if default != None:
        name += f' = {default}'

    name += ') -> ProjectDescription.SettingsDictionary'
    return name

def _default_value(s: Setting) -> Optional[str]:

    if s.default_value == None:
        return None

    default_value = _masked(s.default_value)
    
    if s.type == 'String' or s.type == 'Path':
        return f'\"{default_value}\"'
    elif s.type == 'StringList' or s.type == 'PathList':
        argList = ''
        for a in default_value.split():
            argList += f'\"{a}\", '
        argList = argList[:-2]
        return f'[{argList}]'
    elif s.type == 'Boolean':
        if default_value == "YES":
            return 'true'
        else:
            return 'false'
    elif s.type == 'Enumeration':
        if default_value.startswith('$('):
            return None
        return  f'.{_enum_case_name(default_value)}'

def _masked(text: str) -> str:
    return text.replace('"','\\"')

def _save_value_statement(s: Setting) -> str:
    if s.type == 'String':
        return '.string(value)'
    elif s.type == 'StringList':
        return '.array(values)'
    elif s.type == 'Path':
        return '.string(path)'
    elif s.type == 'PathList':
        return '.array(paths)'
    elif s.type == 'Boolean':
        return '.init(booleanLiteral: bool)'
    elif s.type == 'Enumeration':
        return '.string(value.rawValue)'