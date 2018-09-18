from .parser import TypeStrGrammar


class TypeStr:
    _KNOWN_PARENTS = {
        'list': 'typing.List',
        'dict': 'typing.Dict',
        'tuple': 'typing.Tuple',
    }

    def __init__(self, type_str):
        if not isinstance(type_str, str):
            type_str = str(type_str)
        self._str = type_str
        self._pt_obj = None

    def __str__(self):
        return self._str

    def __repr__(self):
        return f"<{self.__class__.__name__} {self._str!r}>"

    @property
    def _pt(self):
        if self._pt_obj is None:
            self._pt_obj = TypeStrGrammar.simple_parse(self._str)
        return self._pt_obj

    @property
    def name(self):
        return self._pt['name']

    @property
    def args(self):
        return self._pt['args']

    def is_of(self, base_tp) -> bool:
        if not isinstance(base_tp, TypeStr):
            base_tp = TypeStr(base_tp)
        if self.name == base_tp.name:
            return True
        if self.name in self._KNOWN_PARENTS and self._KNOWN_PARENTS[self.name] == base_tp.name:
            return True
        return False


def is_of_type(tp, base_tp) -> bool:
    return TypeStr(tp).is_of(TypeStr(base_tp))
