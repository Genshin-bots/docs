#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import inspect
from pathlib import Path
from collections import UserDict
from typing import Any, Callable, List, Tuple, Union

FILE_PATH = Path(__file__)
TABLE_HEADER = ('参数', '类型', '默认值', '注释')


class DescManager(UserDict):
    def load(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            desc_map = {
                k: v.replace('\\n', '\n') for k, v in re.findall('(.*?)=(.*)', f.read())
            }
        self.update(desc_map)
        return desc_map

    def save(self):
        with open(self.path, 'w+', encoding='utf-8') as f:
            f.write(
                '\n'.join(f'{k}={repr(v.strip())[1:-1]}' for k, v in self.items())
            )

    def get(self, key: str, default=''):
        if key not in self.keys():
            self[key] = default
            self.save()
        return super().get(key, default).strip()

    def __init__(self, desc_path: Union[str, Path]):
        if not isinstance(desc_path, Path):
            desc_path = Path(desc_path)
        if not desc_path.exists():
            if not desc_path.parent.exists():
                desc_path.parent.mkdir(parents=True)
            desc_path.touch()
        self.path = desc_path
        super().__init__()
        self.load()


DESC = DescManager('./doc.description.properties')


def get_members(obj) -> list:
    return [_ for _ in inspect.getmembers(obj) if not _[0].startswith('_')]


def get_super_classes(__cls) -> list:
    return [_ for _ in inspect.getmro(__cls) if _.__name__ != __cls.__name__]


def type2string(__tp) -> str:
    if getattr(__tp, "__args__", None):
        args = ", ".join(type2string(arg) for arg in __tp.__args__)
        return f"{__tp.__name__}[{args}]"
    if isinstance(__tp, (tuple, set)):
        args = ", ".join(__tp)
        return f"Union[{args}]"
    if getattr(__tp, "__module__", None) == "builtins":
        return __tp.__name__
    if inspect.isclass(__tp):
        return __tp.__name__
    return repr(__tp)


def get_fixed_table(*line) -> List[tuple]:
    max_cols = max(len(l_) for l_ in line)
    return [l_ if len(l_) == max_cols else l_ + tuple([''] * (max_cols - len(l_))) for l_ in line]


def format_params(params_source_line: str, padding=4) -> str:
    split_source_line = re.split('\((.*)\)', params_source_line)
    print(split_source_line)
    PADDING = ' ' * padding
    formatted_args = '\n'.join(f'{PADDING}{_.strip()},' for _ in split_source_line[1].split(','))
    return '\n'.join([
        '```python', f'{split_source_line[0]}(', f'{formatted_args}\n):',
        *filter(lambda x: x!= ':', split_source_line[2:]), f'{PADDING}...','```'
    ])


def gen_table(*line: tuple) -> str:
    line = get_fixed_table(*line)
    header_line = line[0]
    col_widths = [max(len(str(row[i])) for row in line) for i in range(len(header_line))]
    table_contents = [
        '| ' + ' '.join(f'{str(_): <{col_widths[pos] + 1}}|' for pos, _ in enumerate(row))
        for row in line
    ]
    table_separate = '|' + ''.join(f'{"-" * (col_widths[pos] + 2)}|' for pos, _ in enumerate(header_line))
    return '\n'.join([table_contents[0], table_separate, *table_contents[1:]])


def get_desc_path(function_: Any, *additional) -> str:
    qualname = function_.__qualname__ if '__init__' not in function_.__qualname__ else ''.join(
        filter(lambda x: x != '__init__', function_.__qualname__.split('.'))
    )
    if hasattr(function_, 'fget'):
        _callable_path = Path(inspect.getsourcefile(function_.fget)).as_posix()
    else:
        _callable_path = Path(inspect.getsourcefile(function_)).as_posix()
    if 'site-packages' in _callable_path:
        _relative_path = '@' + _callable_path[_callable_path.find('site-packages') + 14:]
    else:
        if Path(_callable_path).is_relative_to(FILE_PATH):
            _relative_path = Path(_callable_path).relative_to(FILE_PATH).as_posix()
        else:
            if hasattr(function_, 'fget'):
                return '.'.join([inspect.getmodule(function_).__name__, qualname, *additional])
            elif hasattr(function_, '__qualname__'):
                return '.'.join([inspect.getmodule(function_).__name__, qualname, *additional])
            else:
                return '.'.join([inspect.getmodule(function_).__name__, qualname, *additional])
    return '.'.join([
        *[_[:-3] if _.endswith('.py') else _ for _ in _relative_path.split('/')],
        qualname, *additional
    ])


def get_table(__fm: Callable, is_method=False) -> Union[List[Tuple[str]], None]:
    full_args = inspect.getfullargspec(__fm)
    if not full_args.args:
        return None
    _raw_table = []
    default_values_map = dict(zip(full_args.args, full_args.defaults)) if full_args.defaults else {}
    if full_args.kwonlyargs:
        arg_sequence = [*full_args.args, full_args.varargs, *full_args.kwonlyargs]
        if full_args.kwonlydefaults:
            default_values_map.update(full_args.kwonlydefaults)
    else:
        arg_sequence = full_args.args
        if full_args.varargs:
            arg_sequence.append(full_args.varargs)
    if full_args.varkw:
        arg_sequence.append(full_args.varkw)
    if is_method and arg_sequence[0] in ['self', 'cls']:
        arg_sequence = arg_sequence[1:]
    for _ in arg_sequence:
        _table_row = [str(_)]
        if full_args.annotations:
            _arg_annotation = full_args.annotations.get(_, None)
            _table_row.append(
                type2string(_arg_annotation) if _arg_annotation else ''
            )
        if default_values_map:
            _arg_default_value = default_values_map.get(_, None)
            _table_row.append(
                repr(_arg_default_value) if _arg_default_value else ''
            )
        _table_row.append(
            DESC.get(get_desc_path(__fm, _))
        )
        _raw_table.append(tuple(_table_row))
    return _raw_table


def gen_method_md(method: Any) -> Union[str, None]:
    if inspect.ismethod(method):
        _method_type = 'clsmethod'
    elif inspect.isdatadescriptor(method):
        _method_type = 'property'
    elif inspect.isfunction(method):
        if inspect.getfullargspec(method).args[0] == 'self':
            _method_type = 'method'
        else:
            _method_type = 'staticmethod'
    else:
        return None
    async_state = 'async ' if inspect.iscoroutinefunction(method) else ''
    if _method_type == 'property':
        content = [f'### `{async_state}{_method_type}` {method.fget.__name__}']
    else:
        content = [f'### `{async_state}{_method_type}` {method.__name__}']
        raw_table = get_table(method, is_method=True)
        if raw_table:
            source_arg = inspect.getsource(method).split('\n')[0].strip()
            content.extend([
                f'`{source_arg} ...`' if len(source_arg) < 80 else format_params(source_arg),
                gen_table(*[TABLE_HEADER[:len(raw_table[0])], *raw_table])
            ])
    desc_path = get_desc_path(method, '@description')
    if method.__doc__:
        doc_string = '\n'.join(_.strip() for _ in method.__doc__.split('\n'))
        content.append(DESC.get(desc_path, default=doc_string))
    else:
        content.append(DESC.get(desc_path))
    return '\n\n'.join(content)


def gen_class_md(cls) -> str:
    try:
        super_class_methods = []
        for super_class_ in filter(lambda x: 'abc' not in x.__name__.lower(), get_super_classes(cls)):
            super_class_methods.extend([m[0] for m in get_members(super_class_)])
        super_class_methods = list(set(super_class_methods))
    except AttributeError:
        pass
    class_doc = [f'## `class` {cls.__name__}']
    if hasattr(cls, '__init__'):
        class_doc.append(gen_method_md(cls.__init__))

    for name_, obj_ in filter(lambda x: x[0] not in super_class_methods, get_members(cls)):
        md = gen_method_md(obj_)
        if not md:
            md = f'### `instance` {name_}\n\n' + DESC.get(get_desc_path(obj_, '@description'))
        class_doc.append(md)

    return '\n\n'.join(class_doc)


def gen_function_md(function: Any) -> str:
    async_state = 'async ' if inspect.iscoroutinefunction(function) else ''
    content = [f'## `{async_state}function` {function.__name__}']
    raw_table = get_table(function, is_method=True)
    if raw_table:
        source_arg = inspect.getsource(function).split('\n')[0].strip()
        content.extend([
            f'`{source_arg} ...`' if len(source_arg) < 80 else format_params(source_arg),
            gen_table(*[TABLE_HEADER[:len(raw_table[0])], *raw_table])
        ])
    desc_path = get_desc_path(function, '@description')
    if function.__doc__:
        doc_string = '\n'.join(_.strip() for _ in function.__doc__.split('\n'))
        content.append(DESC.get(desc_path, default=doc_string))
    else:
        content.append(DESC.get(desc_path))
    return '\n\n'.join(content)


if __name__ == '__main__':
    from argparse import ArgumentParser
    from pathlib import Path
    import importlib
    import pkgutil
    import sys

    skip_modules = []
    FILE_PATH = Path(__file__).parent
    WORK_PATH = Path('.')
    SEARCH_PATH = [FILE_PATH.absolute(), WORK_PATH.absolute()]

    parser = ArgumentParser()
    parser.add_argument('module', action='store', help='Name of the module')
    parser.add_argument('--search-paths', '-S', action='append', help='Add a search path.')
    parser.add_argument('--skip', '-s', action='append', help='Specify which module will be skipped.')
    parser.add_argument('--dir', '-d', action='store', help='Specify the directory to store documents.')

    argv = parser.parse_args()
    if argv.search_paths:
        SEARCH_PATH.extend(Path(_).absolute() for _ in argv.search_paths)
    sys.path.extend(str(_) for _ in SEARCH_PATH)
    if argv.skip:
        for s in argv.skip:
            if ',' in s:
                skip_modules.extend(_.strip() for _ in s.split(','))
            else:
                skip_modules.append(s)
    module = importlib.import_module(argv.module)
    module_docs_path = WORK_PATH / 'docs_output' / module.__name__ if not argv.dir else Path(argv.dir)
    if not module_docs_path.exists():
        module_docs_path.mkdir(parents=True)

    md_docs = []
    for import_path, module_name, is_package in pkgutil.walk_packages(module.__path__):
        if module_name in skip_modules:
            continue
        try:
            _sub_module = importlib.import_module(f'{module.__name__}.{module_name}')
        except ModuleNotFoundError as e:
            print(e.name, str(e))
            continue
        for name, member in get_members(_sub_module):
            try:
                if inspect.isclass(member):
                    md_docs.append(gen_class_md(member))
                elif inspect.isfunction(member):
                    md_docs.append(gen_function_md(member))
                else:
                    md_docs.append(
                        f'### `instance` {name}\n\n' + DESC.get(get_desc_path(member, '@description'))
                    )
            except (TypeError, AttributeError):
                pass
        with open(module_docs_path / f'{module_name}.md', 'w+', encoding='utf-8') as f:
            f.write('\n\n'.join(md_docs))
