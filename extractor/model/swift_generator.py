"""This module provides methods to generate Swift code from settings."""
from re import sub
from typing import Optional, List
from .setting import Setting
from .swift_acronyms import ACRONYMS
from .swift_key_replacements import KEY_REPLACEMENTS
from .setting_blacklist import SETTING_BLACKLIST

_TAB = '    '
_EMPTY_LINE = '\n'
_INFOPLIST_KEY = 'INFOPLIST_KEY'

def to_swift_code(settings: List[Setting], xcversion: str) -> str:
    """Generates swift code from a list of settings."""
    string = ''

    string += _fileheader()

    string += _EMPTY_LINE
    
    string += _newline(f'// Generated for Xcode version {xcversion}')
    string += _newline('public extension SettingsDictionary {')
    string += _EMPTY_LINE
    string += _build_settings_enum(settings, 1)
    string += _EMPTY_LINE
    string += _newline('}')

    string += _EMPTY_LINE

    string += _newline('public extension SettingsDictionary {')
    string += _EMPTY_LINE
    string += _argument_enums(settings, 1)
    string += _EMPTY_LINE
    string += _newline('}')

    string += _EMPTY_LINE
    
    string += _add_initialiser_extension()

    return string

def _documentation(text: str) -> str:
    return '/// ' + text

def _fileheader() -> str:
    string = ''
    string += _newline('import ProjectDescription')
    string += _EMPTY_LINE
    string += _newline('public typealias Path = String')
    return string

def _build_settings_enum(settings: List[Setting], indent: int = 0) -> str:
    string = ''
    string += _newline('enum XcodeBuildSetting {', indent)
    for s in settings:
        if s.key in SETTING_BLACKLIST:
            continue
        if s.description != None:
            for line in s.description.split('\n'):
                string += _newline(_documentation(line), indent + 1)
        
        string += _newline(_setting_enum_name(s), indent + 1)
    
    string += _EMPTY_LINE
    string += _settings_var(settings, indent + 1)
    string += _newline('}', indent)
    return string

def _settings_var(settings: List[Setting], indent: int = 0) -> str:
    string = ''
    string += _newline('var info: (key: String, value: SettingValue) {', indent)
    string += _newline('switch self {', indent + 1)
    for s in settings:
        if s.key in SETTING_BLACKLIST:
            continue
        string += _newline(f'case .{_enum_case_for_key(s.key)}(let value):', indent + 2)
        string += _newline(f'return (\"{s.key}\", {_save_value_statement(s=s, valueID="value")})', indent + 3)
    string += _newline('default:', indent + 2)
    string += _newline('fatalError("Not a valid build setting")', indent + 3)

    string += _newline('}', indent + 1)
    string += _newline('}', indent)
    return string

def _argument_enums(settings: List[Setting], indent: int = 0) -> str:
    enums = [_argument_enum(s, indent) for s in settings if s.type == Setting.TYPE_ENUM]
    return _EMPTY_LINE.join(enums)

def _add_initialiser_extension(indent: int = 0) -> str:
    return '''
extension SettingsDictionary: ExpressibleByArrayLiteral {

    public init(buildSettings: [XcodeBuildSetting]) {
        self.init()
        buildSettings.forEach { self[$0.info.key] = $0.info.value }
    }

    public init(arrayLiteral elements: XcodeBuildSetting...) {
        self.init()
        elements.forEach { self[$0.info.key] = $0.info.value }
    }

    public func extend(with buildSettings: [XcodeBuildSetting]) -> ProjectDescription.SettingsDictionary {
        var newDict = self
        buildSettings.forEach { newDict[$0.info.key] = $0.info.value }
        return newDict
    }

    mutating public func extending(with buildSettings: [XcodeBuildSetting]) {
        buildSettings.forEach { self[$0.info.key] = $0.info.value }
    }

}
    '''

def _newline(text: str, indent: int = 0) -> str:
    return _TAB * indent + text + '\n'

def _setting_enum_name(s: Setting):
    name = 'case ' + _enum_case_for_key(s.key)
    name += '('
    s_type = s.type.lower()
    if s_type == Setting.TYPE_STRING.lower():
        name += '_ value: String'
    elif s_type == Setting.TYPE_STRINGLIST.lower():
        name += '_ values: [String]'
    elif s_type == Setting.TYPE_PATH.lower():
        name += '_ path: Path'
    elif s_type == Setting.TYPE_PATHLIST.lower():
        name += '_ paths: [Path]'
    elif s_type == Setting.TYPE_BOOLEAN.lower():
        name += '_ bool: Bool'
    elif s_type == Setting.TYPE_ENUM.lower():
        name += f'_ value: {_argument_enum_name(s.key)}'

    default = _default_value(s)
    if default != None:
        name += f' = {default}'

    name += ')'
    return name

def _argument_enum(s: Setting, indent: int = 0) -> str:
    if s.enum_cases == None:
        return ''
    string = ''
    string += _newline(f'enum {_argument_enum_name(s.key)}: String' + ' {', indent)

    for v in s.enum_cases:
        string += _newline(f'case {_argument_enum_case_name(v)} = \"{v}\"', indent + 1)

    string += _newline('}', indent)
    return string

def _argument_enum_name(name: str) -> str:
    string = _camel_case(name, start_lower=False)
    return string + 'Value'

def _argument_enum_case_name(name: str) -> str:
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
    elif 'c++' in name:
        n = sub(r"c\+\+", "c_Plus_Plus", name)
        return _camel_case(n)
    elif 'gnu++' in name:
        n = sub(r"gnu\+\+", "gnu_Plus_Plus", name)
        return _camel_case(n)
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
        return  f'.{_argument_enum_case_name(default_value)}'

def _masked(text: str) -> str:
    return text.replace('"','\\"')

def _save_value_statement(s: Setting, valueID: str) -> str:
    s_type = s.type.lower()
    if s_type == Setting.TYPE_STRING.lower():
        return f'.string({valueID})'
    elif s_type == Setting.TYPE_STRINGLIST.lower():
        return f'.array({valueID})'
    elif s_type == Setting.TYPE_PATH.lower():
        return f'.string({valueID})'
    elif s_type == Setting.TYPE_PATHLIST.lower():
        return f'.array({valueID})'
    elif s_type == Setting.TYPE_BOOLEAN.lower():
        return f'.init(booleanLiteral: {valueID})'
    elif s_type == Setting.TYPE_ENUM.lower():
        return f'.string({valueID}.rawValue)'

def _enum_case_for_key(key: str) -> str:
    comps = list(sub(r"(_|-|\.|\+)+", " ", key).split(" "))
    if key.startswith(_INFOPLIST_KEY):
        nameComps = ['infoPlistKey'] + comps[2:]
        name = ''.join(nameComps)
        return name

    corrected_comps = []
    for c in comps:
        if ACRONYMS.get(c) is not None:
            corrected_comps += ACRONYMS.get(c)
        elif c in KEY_REPLACEMENTS:
            return _decapitalize(c)
        else:
            corrected_comps.append(c.title())
    corrected_comps[0] = str(corrected_comps[0]).lower()
    name = ''.join(corrected_comps)
    return name

def _decapitalize(s):
    return ''.join([s[:1].lower(), s[1:]]) 