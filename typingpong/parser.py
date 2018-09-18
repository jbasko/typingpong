from shreducer.tokenizers import create_shlex_tokenizer
import string
import shreducer


def unquote(s):
    if s and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    return s


class TypeStrGrammar(shreducer.Grammar):
    class t:
        IDENT = None
        BRACKETS_OPEN = '['
        BRACKETS_CLOSE = ']'
        PARENS_OPEN = '('
        PARENS_CLOSE = ')'
        TAG_OPEN = '<'
        TAG_CLOSE = '>'
        COMMA = ','
        ARGS_LIST_ITEMS = ()
        TYPE_DEF = ()
        SCOPE_REFERENCE = ()

    @classmethod
    def get_default_tokenizer(cls):
        return create_shlex_tokenizer(
            wordchars=string.ascii_uppercase + string.ascii_lowercase + string.digits + '_."\'',
        )

    @classmethod
    def get_rules(cls):
        """
        Argument list aggregation can only start once we see the closing bracket.
        """
        return [
            (
                [cls.t.IDENT],
                cls.create_primitive_type_def,
            ),
            (
                [cls.t.TYPE_DEF, cls.t.BRACKETS_CLOSE],
                cls.create_args_list_items,
            ),
            (
                [cls.t.TYPE_DEF, cls.t.COMMA, cls.t.ARGS_LIST_ITEMS, cls.t.BRACKETS_CLOSE],
                cls.prepend_to_args_list_items,
            ),
            (
                [cls.t.TYPE_DEF, cls.t.BRACKETS_OPEN, cls.t.ARGS_LIST_ITEMS, cls.t.BRACKETS_CLOSE],
                cls.create_composite_type_def,
            ),
            (
                [cls.t.TYPE_DEF, cls.t.PARENS_OPEN, cls.t.TYPE_DEF, cls.t.PARENS_CLOSE],
                cls.create_forward_reference,
            ),
            (
                [cls.t.TAG_OPEN, cls.t.TYPE_DEF, cls.t.TYPE_DEF, cls.t.TAG_CLOSE],
                cls.create_class_reference,
            ),
            (
                [cls.t.TAG_OPEN, cls.t.TYPE_DEF, cls.t.TAG_CLOSE],
                cls.process_scope_reference,
            ),
            (
                [cls.t.TYPE_DEF, cls.t.SCOPE_REFERENCE, cls.t.TYPE_DEF],
                cls.merge_scope_reference,
            ),
        ]

    @classmethod
    def create_primitive_type_def(cls, types, values):
        type_name, = values
        return [cls.t.TYPE_DEF], [{'name': type_name, 'args': None}]

    @classmethod
    def create_args_list_items(cls, types, values):
        type_def, brackets_close = values
        return [cls.t.ARGS_LIST_ITEMS, cls.t.BRACKETS_CLOSE], [[type_def], brackets_close]

    @classmethod
    def prepend_to_args_list_items(cls, types, values):
        type_def, _, args_list_items, brackets_close = values
        args_list_items.insert(0, type_def)
        return [cls.t.ARGS_LIST_ITEMS, cls.t.BRACKETS_CLOSE], [args_list_items, brackets_close]

    @classmethod
    def create_composite_type_def(cls, types, values):
        type_def, brackets_open, args_list_items, brackets_close = values
        return [cls.t.TYPE_DEF], [{'name': type_def['name'], 'args': args_list_items}]

    @classmethod
    def create_forward_reference(cls, types, values):
        fw_reference, _, name, _ = values
        name = unquote(name['name'])
        return [cls.t.TYPE_DEF], [{'name': name, 'args': None, 'forward_reference': True}]

    @classmethod
    def create_class_reference(cls, types, values):
        _, class_keyword, class_name, _ = values
        name = unquote(class_name['name'])
        return [cls.t.TYPE_DEF], [{'name': name, 'args': None, 'class_reference': True}]

    @classmethod
    def process_scope_reference(cls, types, values):
        """
        by scope reference we mean "<locals>" in this:
            "tests.test_parser.test_user_class.<locals>.C"
        """
        _, name, _ = values
        return [cls.t.SCOPE_REFERENCE], [f"<{name['name']}>"]

    @classmethod
    def merge_scope_reference(cls, types, values):
        prefix, scope_reference, suffix = values
        return [cls.t.TYPE_DEF], [{'name': f"{prefix['name']}{scope_reference}{suffix['name']}", 'args': None}]
