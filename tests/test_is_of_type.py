import typing

from typingpong.type_str import is_of_type


def test_is_of_type():
    class C:
        pass

    assert is_of_type(list, typing.List)
    assert is_of_type(typing.List, typing.List)
    assert is_of_type(typing.List, typing.List[str])
    assert is_of_type(typing.List, typing.List[C])
    assert is_of_type(typing.List, typing.List["C"])

    assert not is_of_type(typing.List, typing.Dict)
    assert not is_of_type(typing.List, typing.Dict[str, typing.List])
    assert not is_of_type(dict, typing.List)
    assert not is_of_type(dict, typing.List[dict])

    assert is_of_type(dict, typing.Dict)
    assert is_of_type(dict, typing.Dict[str, str])
    assert is_of_type(typing.Dict, typing.Dict[str, str])
    assert is_of_type(typing.Dict, typing.Dict[str, "Unknown"])
    assert is_of_type(typing.Dict, typing.Dict[str, C])
    assert is_of_type(typing.Dict, typing.Dict[str, "C"])
    assert is_of_type(typing.Dict, typing.Dict[str, typing.List["C"]])
    assert is_of_type(typing.Dict, typing.Dict[str, typing.List[C]])
