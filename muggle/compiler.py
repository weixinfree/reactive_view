from parser import component
from typing import Callable
from pathlib import Path
import os


DST = None
SRC = None


def _read(f: str) -> str:
    with open(f, encoding='utf-8') as file:
        return file.read()


def _parse(dsl: str):
    return component.parse_strict(dsl)


def _check(d: Path):
    if not (d.exists() and d.is_dir()):
        raise SystemExit(f'{d} not a leggal directory')
    return d


def _get_filename_without_suffix(file: Path) -> str:
    return file.name.rsplit('.', maxsplit=1)[0]


def _get_dst_file(file: Path) -> Path:
    segs = str(file).split('/')[1:-1]

    dst = DST
    for seg in segs:
        dst = dst.joinpath(seg)

    return dst.joinpath(_get_filename_without_suffix(file) + '.rvc')


class _Generator:

    def identifier(self, ast, code: Callable[[str], None]):
        code(f'PUSH {ast}')

    def unit(self, ast, code: Callable[[str], None]):
        _, value, unit = ast
        code(f'PUSH {unit}')
        code(f'PUSH {value}')
        code(f'UNIT')

    def prop(self, ast, code: Callable[[str], None]):
        obj, f, *fields = ast[1]
        code(f'PUSH {obj}')
        code(f'PUSH {f}')
        code(f'PROP')
        for field in fields:
            code(f'PUSH {field}')
            code(f'PROP')

    def res_ref(self, ast, code: Callable[[str], None]):
        _, _type, _name = ast
        code(f'PUSH {_name}')
        code(f'PUSH {_type}')
        code(f'RES')

    def func(self, ast, code: Callable[[str], None]):
        _, f_name, args = ast
        if args:
            if '$' in args:
                code(f'DUP')
                code(f'STORE_TEMP')

            for arg in args[::-1]:
                if arg == '$':
                    code(f'PUSH_TEMP')
                else:
                    code(f'PUSH {arg}')

        code(f'CALL {f_name}')

    def callback(self, ast, code: Callable[[str], None]):
        _, params, prop = ast
        instructions = []
        _code = instructions.append
        for p in params:
            _code(f'PUSH f{p}')
        _translate(prop, _code)

        insturcts = ">".join(instructions)
        code(f'CALLBACK {insturcts}')

    def pipe(self, ast, code: Callable[[str], None]):
        _, pipes = ast
        for p in pipes:
            _translate(p, code)

    def include(self, ast, code: Callable[[str], None]):
        _, component = ast
        link = SRC.joinpath(component)
        _process(link)
        dst = _get_dst_file(link)
        code(f'INCLUDE {dst}')

    def computed_value(self, ast, code: Callable[[str], None]):
        _, express = ast
        _translate(express, code)

    def attr(self, ast, code: Callable[[str], None]):
        _, attr_name, attr_value = ast
        _translate(attr_value, code)
        code(f'ATTR {attr_name}')

    def component(self, ast, code: Callable[[str], None]):
        _, component, attrs = ast
        code(f'NEW {component}')
        for _attr in attrs:
            _translate(_attr, code)


_generator = _Generator()


def _translate(ast, code: Callable[[str], None]):
    if isinstance(ast, tuple):
        getattr(_generator, ast[0])(ast, code)
    else:
        assert isinstance(ast, str), str(ast) + ' is not string'
        _generator.identifier(ast, code)


def _process(file):
    if not file.exists():
        raise SystemExit(f'{file} not exists')

    dst = _get_dst_file(file)

    if not dst.parent.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.is_file():
        return

    ast = _parse(_read(file))
    instructions = []
    code = instructions.append
    _translate(ast, code)

    with open(dst, encoding='utf-8', mode='w') as f:
        f.write('\n'.join(instructions))


def compile(src, dst):
    global SRC, DST
    SRC = _check(Path(src))
    DST = _check(Path(dst))

    for rvc in DST.glob('**/*.rvc'):
        os.remove(rvc)

    for rv in SRC.glob('**/*.rv'):
        _process(rv)


if __name__ == '__main__':
    import fire
    fire.Fire(compile)
