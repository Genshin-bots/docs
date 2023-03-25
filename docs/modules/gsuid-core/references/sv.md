---
title: SV
description: sv 模块
---

## `class` SVList

## `class` SV

服务注册器

```python
def __init__(
    self,
    name: str = '',
    pm: int = 3,
    priority: int = 5,
    enabled: bool = True,
    area: Literal['GROUP', 'DIRECT', 'ALL'] = 'ALL',
    black_list: List = [],
)
```

| 参数         | 类型     | 默认值    | 注释    |
|------------|:-------|--------|-------|
| name       | `str`  | 无      | 服务的名称 |
| pm         | `int`  | `3`    | 用户权限  |
| priority   | `int`  | `5`    | 响应优先级 |
| enabled    | `bool` | `True` | 启用状态  |
| area       | `int`  | `5`    | 作用范围  |
| black_list | `int`  | `5`    | 黑名单列表 |

### `method` on_fullmatch

#### 参数列表

`def on_fullmatch(self, keyword: Union[str, Tuple[str, ...]], block: bool = False)`

| 参数      | 类型                            | 默认值     |
|---------|:------------------------------|---------|
| keyword | `Union[str, Tuple[str, ...]]` | 无       |
| block   | `bool`                        | `False` |

全字匹配消息。

### `method` on_prefix

#### 参数列表

`def on_fullmatch(self, keyword: Union[str, Tuple[str, ...]], block: bool = False)`

| 参数      | 类型                            | 默认值     |
|---------|:------------------------------|---------|
| keyword | `Union[str, Tuple[str, ...]]` | 无       |
| block   | `bool`                        | `False` |

匹配消息前缀。

### `method` on_suffix

#### 参数列表

`def on_fullmatch(self, keyword: Union[str, Tuple[str, ...]], block: bool = False)`

| 参数      | 类型                            | 默认值     |
|---------|:------------------------------|---------|
| keyword | `Union[str, Tuple[str, ...]]` | 无       |
| block   | `bool`                        | `False` |

全字消息后缀。

### `method` on_keyword

#### 参数列表

`def on_fullmatch(self, keyword: Union[str, Tuple[str, ...]], block: bool = False)`

| 参数      | 类型                            | 默认值     |
|---------|:------------------------------|---------|
| keyword | `Union[str, Tuple[str, ...]]` | 无       |
| block   | `bool`                        | `False` |

全字匹配消息关键字。

### `method` on_command

#### 参数列表

`def on_fullmatch(self, keyword: Union[str, Tuple[str, ...]], block: bool = False)`

| 参数      | 类型                            | 默认值     |
|---------|:------------------------------|---------|
| keyword | `Union[str, Tuple[str, ...]]` | 无       |
| block   | `bool`                        | `False` |

全字匹配消息命令。

## `value` SL

服务列表。是一个[SVList](#class-svlist)对象。