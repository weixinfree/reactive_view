import sys
import os
muggle = os.path.dirname(os.path.dirname(__file__))
print(muggle)
sys.path.append(muggle)

from muggle import *


def test_identifier():
    assert identifier.parse('30dp') == '30dp'


def test_unit():
    assert unit.parse('30dp') == ('unit', 30, 'dp')
    assert unit.parse('30px') == ('unit', 30, 'px')
    assert unit.parse('100sp') == ('unit', 100, 'sp')


def test_include():
    result = include.parse('include(hello.rv)')
    assert result == ('include', 'hello.rv')

    result = include.parse('include( ../../hello.rv )')
    assert result == ('include', '../../hello.rv')


def test_prop():
    result = prop.parse('user.name.hello')
    assert result == ('prop', ['user', 'name', 'hello'])


def test_ref_ref():
    result = res_ref.parse('@string/welcome')
    assert result == ('res_ref', 'string', 'welcome')

    result = res_ref.parse('@drawable/contine_gift_send_btn_bg_dark')
    assert result == ('res_ref', 'drawable', 'contine_gift_send_btn_bg_dark')


def test_func():
    result = func.parse('scale $, 40dp, 30dp')
    assert result == ('func', 'scale', ['$', '40dp', '30dp'])


def test_func_simple():
    result = func.parse('scale')
    assert result == ('func', 'scale', [])


def test_callback():
    result = callback.parse('_ -> user.onClick')
    assert result == ('callback', ['_'], ('prop', ['user', 'onClick']))

    result = callback.parse('view, position -> user.onClick')
    assert result == ('callback', ['view', 'position'], ('prop', ['user', 'onClick']))


def test_pipe_call():
    result = pipe_call.parse('30 |> dp')
    assert result == ('pipe', ['30', ('func', 'dp', [])])

    result = pipe_call.parse('30 |> scale $, 30dp, 40dp')
    assert result == ('pipe', ['30', ('func', 'scale', ['$', '30dp', '40dp'])])

    result = pipe_call.parse('user.portrait |> scale $, 30dp, 40dp')
    assert result == ('pipe', [('prop', ['user', 'portrait']), ('func', 'scale', ['$', '30dp', '40dp'])])


def test_computed_value():
    result = computed_value.parse('{30dp}')
    assert result == ('computed_value', ('unit', 30, 'dp'))

    result = computed_value.parse('{user.name}')
    assert result == ('computed_value', ('prop', ['user', 'name']))

    result = computed_value.parse('{ user.sex.length }')
    assert result == ('computed_value', ('prop', ['user', 'sex', 'length']))

    result = computed_value.parse('{v -> v.name}')
    assert result == ('computed_value', ('callback', ['v'], ('prop', ['v', 'name'])))

    result = computed_value.parse('{30dp |> large $, 2}')
    assert result == ('computed_value', ('pipe', [('unit', 30, 'dp'), ('func', 'large', ['$', '2'])]))


def test_attr():
    result = attr.parse('w: match')
    assert result == ('attr', 'w', 'match')

    result = attr.parse('h : wrap')
    assert result == ('attr', 'h', 'wrap')

    result = attr.parse('textSize: 13sp')
    assert result == ('attr', 'textSize', ('unit', 13, 'sp'))

    result = attr.parse('text: @string/default_user_name')
    assert result == ('attr', 'text', ('res_ref', 'string', 'default_user_name'))

    result = attr.parse('text: {user.name}')
    assert result == ('attr', 'text', ('computed_value', ('prop', ['user', 'name'])))

    result = attr.parse('click: {v -> user.changeName}')
    assert result == ('attr', 'click', ('computed_value', ('callback', ['v'], ('prop', ['user', 'changeName']))))


def test_component():
    result = component.parse('Image {}')
    assert result == ('component', 'Image', [])

    result = component.parse('View {w: match, h: wrap}')
    assert result == ('component', 'View', [('attr', 'w', 'match'), ('attr', 'h', 'wrap')])

    nest_component = r'''Column {
    w: match, h: wrap
    gravity: center_horiontal
    child: Text {
        w: 40dp
        h: wrap
        textSize: 13sp
        text: {user.name}
    },
    child: Image {
        w: wrap
        h: wrap
        scaleType: fitCenter
        src: {user.portrait |> default DEFAULT_POTRAIT}
    }
}
'''
    result = component.parse(nest_component)
    assert result == (
        'component', 'Column',
        [('attr', 'w', 'match'),
         ('attr', 'h', 'wrap'),
         ('attr', 'gravity', 'center_horiontal'),
         ('attr', 'child',
            ('component', 'Text',
                [('attr', 'w', ('unit', 40, 'dp')),
                 ('attr', 'h', 'wrap'),
                 ('attr', 'textSize', ('unit', 13, 'sp')),
                 ('attr', 'text', ('computed_value', ('prop', ['user', 'name'])))])),
         ('attr', 'child',
            ('component', 'Image',
                [('attr', 'w', 'wrap'),
                 ('attr', 'h', 'wrap'),
                 ('attr', 'scaleType', 'fitCenter'),
                 ('attr', 'src',
                    ('computed_value',
                        ('pipe',
                            [('prop', ['user', 'portrait']),
                             ('func', 'default', ['DEFAULT_POTRAIT'])])))]))])


def test_file():
    path = os.path.join(os.path.dirname(__file__), 'dsl.rv')
    with open(path, encoding='utf-8') as f:
        content = f.read()
    result = component.parse(content)
    assert result[0] == 'component'
