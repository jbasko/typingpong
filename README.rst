===========
taipingpong
===========

.. code-block:: python

    import typing
    from typingpong import is_of_type

    assert is_of_type(list, typing.List)
    assert is_of_type(list, typing.List[str])

    assert is_of_type(dict, typing.Dict)
    assert is_of_type(dict, typing.Dict["X", "Y"])
    assert is_of_type(typing.Dict, typing.Dict["X", "Y"])
