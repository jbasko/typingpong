import typing

import pytest

from typingpong.parser import TypeStrGrammar


@pytest.mark.parametrize('input_str,expected', [
    ['str', {'name': 'str', 'args': None}],
    ['typing.List[str]', {'name': 'typing.List', 'args': [{'name': 'str', 'args': None}]}]
])
def test_primitives(input_str, expected):
    assert expected == TypeStrGrammar.simple_parse(input_str)


def test_nested_composite():
    pt = TypeStrGrammar.simple_parse("typing.Union[None, typing.Dict[str, typing.Dict]]")
    assert pt['name'] == 'typing.Union'
    assert pt['args'][0] == {'name': 'None', 'args': None}
    assert pt['args'][1] == {'name': 'typing.Dict', 'args': [
        {'name': 'str', 'args': None},
        {'name': 'typing.Dict', 'args': None},
    ]}


def test_forward_references():
    type_str = str(typing.Tuple["MyType", "YourType"])
    pt = TypeStrGrammar.simple_parse(type_str)
    assert pt['args'][0] == {'name': 'MyType', 'args': None, 'forward_reference': True}
    assert pt['args'][1] == {'name': 'YourType', 'args': None, 'forward_reference': True}


def test_builtin_types():
    type_str = str(list)
    pt = TypeStrGrammar.simple_parse(type_str)
    assert pt == {'name': 'list', 'args': None, 'class_reference': True}


def test_user_class():
    class C:
        pass

    class D:
        pass

    type_str = str(typing.Dict[C, D])

    pt = TypeStrGrammar.simple_parse(type_str)
    assert pt['name'] == 'typing.Dict'
    assert pt['args'][0]['name'].endswith('.C')
    assert pt['args'][0]['args'] is None
    assert pt['args'][1]['name'].endswith('.D')
    assert pt['args'][1]['args'] is None
