from parsec import *

################################
# enhance
################################


def optional(p):
    '''`Make a parser as optional. If success, return the result, otherwise return
    None silently, without raising any exception.
    '''
    @Parser
    def optional_parser(text, index):
        res = p(text, index)
        if res.status:
            return Value.success(res.index, res.value)
        else:
            '''Return None without doing anything.'''
            return Value.success(res.index, None)
    return optional_parser


################################
# component
################################


space = regex(r'\s+', re.MULTILINE)
comma = string(',')
comment = regex(r'#.*')
ignore = many(space | comma | comment)


def lexeme(p):
    return p << ignore


identifier = lexeme(regex(r'[\d\w_$]+'))
dot = string('.')
l_curly_braces = lexeme(string('{'))
r_curly_braces = lexeme(string('}'))
pipe = lexeme(string('|>'))

dp = lexeme(string('dp'))
sp = lexeme(string('sp'))
px = lexeme(string('px'))
num = lexeme(regex(r'\d+')).parsecmap(int)


@generate
def unit():
    _num = yield num
    _unit = yield (dp ^ sp ^ px)
    return ('unit', _num, _unit)


@generate
def res_ref():
    yield string('@')
    res_type = yield identifier
    yield string('/')
    res_name = yield identifier
    yield ignore
    return ('res_ref', res_type, res_name)


@generate
def prop():
    obj = yield identifier
    field_chain = yield many1(dot >> identifier)
    return ('prop', [obj, *field_chain])


@generate
def func():
    f_name = yield identifier
    args = yield optional(many(identifier))
    return ('func', f_name, args or list())


@generate
def callback():
    params = yield many1(identifier)
    yield lexeme(string('->'))
    _callback = yield prop
    return ('callback', params, _callback)


@generate
def pipe_call():
    p = yield (prop ^ unit ^ identifier)
    pipes = yield many1(pipe >> func)
    return ('pipe', [p, *pipes])


@generate
def computed_value():
    yield l_curly_braces
    _value = yield (callback ^ pipe_call ^ prop ^ unit)
    yield r_curly_braces
    return ('computed_value', _value)


@generate
def attr():
    _attr = yield identifier
    yield lexeme(string(':'))
    _value = yield (component ^ computed_value ^ include ^ res_ref ^ unit ^ identifier)
    return ('attr', _attr, _value)


@generate
def component():
    yield ignore
    c_name = yield identifier
    yield l_curly_braces
    attrs = yield (many(attr))
    yield r_curly_braces
    return ('component', c_name, attrs)


################################
# include
################################


@generate
def include():
    yield lexeme(string('include'))
    yield lexeme(string('('))
    name = yield lexeme(regex(r'[\w\d_./$]+'))
    yield lexeme(string(')'))
    return ('include', name)
