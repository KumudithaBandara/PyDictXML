import logging
import numbers
import re
from random import randint
from xml.dom.minidom import parseString

LOG = logging.getLogger("DictToXML")

valid_xml_cache = {}
valid_xml_name_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9._-]*$')
ids = set()


def default_item_func(parent):
    """Return parent node as the default name for list items"""
    return parent


def dicttoxml(
        obj,
        root=True,
        custom_root='root',
        xml_declaration=True,
        ids=False,
        attr_type=True,
        item_func=default_item_func,
        cdata=False,
        include_encoding=True,
        encoding='UTF-8',
        return_bytes=True,
):
    """Converts a python object into XML.
    Arguments:
    - root specifies whether the output is wrapped in an XML root element
      Default is True
    - custom_root allows you to specify a custom root element.
      Default is 'root'
    - ids specifies whether elements get unique ids.
      Default is False
    - attr_type specifies whether elements get a data type attribute.
      Default is True
    - item_func specifies what function should generate the element name for
      items in a list.
      Default is 'item'
    - cdata specifies whether string values should be wrapped in CDATA sections.
      Default is False
    """
    output = []

    if root:
        if xml_declaration:
            if include_encoding:
                output.append(f'<?xml version="1.0" encoding="{encoding}" ?>')
            else:
                output.append('<?xml version="1.0" ?>')

        output.append(f'<{custom_root}>{convert(obj, ids, attr_type, item_func, cdata, parent=custom_root)}'
                      f'</{custom_root}>')
    else:
        output.append(convert(obj, ids, attr_type, item_func, cdata, parent=''))

    output_str = ''.join(output)
    if not return_bytes:
        return output_str
    return output_str.encode('utf-8')


def set_debug(debug=False, filename='dicttoxml.log'):
    if debug:
        import datetime
        print(f'Debug mode is on. Events are logged at: {filename}')
        logging.basicConfig(filename=filename, level=logging.INFO)
        LOG.info(f'\nLogging session starts: {datetime.datetime.now()}')
    else:
        logging.basicConfig(level=logging.WARNING)


def convert_byte_strings(val):
    """Converts byte strings to Unicode strings."""
    if isinstance(val, bytes):
        return val.decode('utf-8')
    return val


def make_id(element, start=100000, end=999999):
    """Returns a random integer"""
    return f"{element}_{randint(start, end)}"


def get_unique_id(element):
    """Returns a unique id for a given element"""
    this_id = make_id(element)
    while this_id in ids:
        this_id = make_id(element)
    ids.add(this_id)
    return this_id


def get_xml_type(val):
    """Returns the data type for the xml type attribute"""
    type_name = type(val).__name__

    if type_name == 'NoneType':
        return 'null'
    elif type_name == 'bool':
        return 'bool'
    elif type_name in ('str', 'unicode'):
        return 'str'
    elif type_name in ('int', 'long'):
        return 'int'
    elif type_name == 'float':
        return 'float'
    elif isinstance(val, numbers.Number):
        return 'number'
    elif isinstance(val, dict):
        return 'dict'
    elif isinstance(val, (list, tuple)):
        return 'list'
    return type_name


def escape_xml(s):
    """
    Escapes special characters in XML.
    """
    if isinstance(s, str):
        s = s.replace('&', '&amp;')
        s = s.replace('"', '&quot;')
        s = s.replace('\'', '&apos;')
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
    return s


def make_attrstring(attr):
    """Returns an attribute string in the form key="val" """
    if not attr:
        return ''

    attr_parts = [f'{k}="{v}"' for k, v in attr.items()]
    attrstring = ' '.join(attr_parts)

    return (' ' if attrstring else '') + attrstring


def convert(obj, ids, attr_type, item_func, cdata, parent='root'):
    """Routes the elements of an object to the right function to convert them
    based on their data type"""
    obj_type_name = type(obj).__name__

    if isinstance(obj, bool):
        return convert_bool(item_func(parent), obj, attr_type, cdata)

    if obj is None:
        return convert_none(item_func(parent), obj, attr_type, cdata)

    if isinstance(obj, (numbers.Number, str)):
        return convert_kv(item_func(parent), obj, attr_type, cdata)

    obj_isoformat = getattr(obj, 'isoformat', None)
    if obj_isoformat is not None:
        return convert_kv(item_func(parent), obj_isoformat(), attr_type, cdata)

    if isinstance(obj, dict):
        return convert_dict(obj, ids, parent, attr_type, item_func, cdata)

    if isinstance(obj, (list, tuple)):
        return convert_list(obj, ids, parent, attr_type, item_func, cdata)

    raise TypeError(f'Unsupported data type: {obj} ({obj_type_name})')


def convert_dict(obj, ids, parent, attr_type, item_func, cdata):
    """Converts a dict into an XML string."""
    output = []

    for key, val in obj.items():
        output.append(convert_dict_item(key, val, ids, parent, attr_type, item_func, cdata))

    return ''.join(output)


def convert_dict_item(key, val, ids, parent, attr_type, item_func, cdata):
    attr = {} if not ids else {'id': str(get_unique_id(parent))}
    key, attr = make_valid_xml_name(key, attr)

    if isinstance(val, bool):
        return convert_bool(key, val, attr_type, cdata, attr)

    elif isinstance(val, (numbers.Number, str)):
        return convert_kv(key, val, attr_type, cdata, attr)

    elif hasattr(val, 'isoformat'):  # datetime
        return convert_kv(key, val.isoformat(), attr_type, cdata, attr)

    elif isinstance(val, (dict, list, tuple)):
        return convert_nested_structure(val, key, ids, attr_type, item_func, cdata, attr)

    elif val is None:
        return convert_none(key, val, attr_type, cdata, attr)

    else:
        raise TypeError(f'Unsupported data type: {val} ({type(val).__name__})')


def convert_nested_structure(val, key, ids, attr_type, item_func, cdata, attr):
    if attr_type:
        attr['type'] = get_xml_type(val)

    if isinstance(val, dict):
        inner_content = convert_dict(val, ids, key, attr_type, item_func, cdata)
    else:
        inner_content = convert_list(val, ids, key, attr_type, item_func, cdata)

    if item_func != default_item_func:
        return f'<{key}{make_attrstring(attr)}>{inner_content}</{key}>'
    return inner_content


def convert_list(items, ids, parent, attr_type, item_func, cdata):
    output = []
    item_name = item_func(parent)
    this_id = get_unique_id(parent) if ids else None

    for i, item in enumerate(items):
        attr = {} if not ids else {'id': f'{this_id}_{i+1}'}

        if isinstance(item, (numbers.Number, str)):
            output.append(convert_kv(item_name, item, attr_type, cdata, attr))

        elif hasattr(item, 'isoformat'):  # datetime
            output.append(convert_kv(item_name, item.isoformat(), attr_type, cdata, attr))

        elif isinstance(item, bool):
            output.append(convert_bool(item_name, item, attr_type, cdata, attr))

        elif isinstance(item, dict):
            inner_content = convert_dict(item, ids, parent, attr_type, item_func, cdata)
            output.append(f'<{item_name}{make_attrstring(attr)}>{inner_content}</{item_name}>')

        elif isinstance(item, (list, tuple)):
            attr_type_str = ' type="list"' if attr_type else ''
            if item_func == default_item_func:
                inner_content = convert_list(item, ids, item_name, attr_type, item_func, cdata)
                output.append(f'<{item_name}{make_attrstring(attr)}{attr_type_str}>{inner_content}</{item_name}>')
            else:
                output.extend(convert_list(item, ids, item_name, attr_type, item_func, cdata))

        elif item is None:
            output.append(convert_none(item_name, None, attr_type, cdata, attr))

        else:
            raise TypeError(f'Unsupported data type: {item} ({type(item).__name__})')

    return ''.join(output)


def convert_kv(key, val, attr_type, cdata=False, attr=None):
    """Converts a number or string into an XML element"""
    if attr is None:
        attr = {}

    key, attr = make_valid_xml_name(key, attr)

    if attr_type:
        attr['type'] = get_xml_type(val)
    attrstring = make_attrstring(attr)
    val_content = wrap_cdata(val) if cdata else escape_xml(val)
    return f'<{key}{attrstring}>{val_content}</{key}>'


def convert_bool(key, val, attr_type, cdata=False, attr=None):
    """Converts a boolean into an XML element"""
    if attr is None:
        attr = {}

    key, attr = make_valid_xml_name(key, attr)

    if attr_type:
        attr['type'] = get_xml_type(val)
    attrstring = make_attrstring(attr)
    return f'<{key}{attrstring}>{str(val).lower()}</{key}>'


def convert_none(key, val, attr_type, cdata=False, attr=None):
    """Converts a null value into an XML element"""
    if attr is None:
        attr = {}

    key, attr = make_valid_xml_name(key, attr)

    if attr_type:
        attr['type'] = get_xml_type(val)
    attrstring = make_attrstring(attr)
    return f'<{key}{attrstring}></{key}>'


def make_valid_xml_name(key, attr):
    """Tests an XML name and fixes it if invalid"""
    key = escape_xml(convert_byte_strings(key))
    attr = escape_xml(convert_byte_strings(attr))

    if key_is_valid_xml(key):
        return key, attr

    if str(key).replace('.', '', 1).isdigit():
        return 'n%s' % key, attr

    if key_is_valid_xml(key.replace(' ', '_')):
        return key.replace(' ', '_'), attr

    attr['name'] = key
    return 'key', attr


def key_is_valid_xml(key):
    """Checks that a key is a valid XML name"""
    if key in valid_xml_cache:
        return valid_xml_cache[key]

    if not valid_xml_name_pattern.match(key):
        valid_xml_cache[key] = False
        return False

    test_xml = f'<?xml version="1.0" encoding="UTF-8" ?><{key}>foo</{key}>'
    try:
        parseString(test_xml)
        valid_xml_cache[key] = True
        return True
    except Exception as e:
        LOG.error(f'Exception in key_is_valid_xml(): {e}')
        valid_xml_cache[key] = False
        return False


def wrap_cdata(val):
    """Wraps a string into CDATA sections"""
    val = convert_byte_strings(val).replace(']]>', ']]]]><![CDATA[>')
    return '<![CDATA[' + val + ']]>'
