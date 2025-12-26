# 类型存根自动生成

本项目使用自动生成的方式创建 `.pyi` 类型存根文件，而不是手动维护。这确保类型定义始终与 C 扩展模块保持同步。

## 工作原理

### 构建流程

1. **构建 C 扩展** - CMake 编译 AprilTag C 库
2. **自动生成 stub** - `generate_stubs.py` 脚本在构建后运行
3. **包含到分发包** - 生成的 `.pyi` 文件自动包含在安装包中

### 文件说明

- **generate_stubs.py** - Stub 生成脚本
  - 在 `setup.py` 构建完成后自动运行
  - 基于模板生成 `apriltag.pyi`
  - 确保 `py.typed` 标记文件存在

- **apriltag.pyi** - 自动生成的类型存根
  - ⚠️ 不要手动编辑此文件
  - 每次构建时会重新生成
  - 包含完整的类型定义和文档

- **py.typed** - PEP 561 标记文件
  - 标识此包支持类型检查
  - 空文件即可

## 修改类型定义

如果需要修改类型定义，应该编辑 `generate_stubs.py` 而不是直接编辑 `apriltag.pyi`。

### 示例：添加新的 tag family

如果 AprilTag C 库添加了新的 tag family，在 `generate_stubs.py` 中更新：

```python
TagFamily = Literal[
    'tag36h11',
    'tag36h10',
    'tag25h9',
    'tag16h5',
    'tagCircle21h7',
    'tagCircle49h12',
    'tagStandard41h12',
    'tagStandard52h13',
    'tagCustom48h12',
    'newTagFamily'  # 添加新的 family
]
```

### 示例：修改函数签名

如果 C 扩展的参数发生变化，在 `generate_stubs.py` 的模板中更新：

```python
def __init__(
    self,
    family: TagFamily,
    threads: int = 1,
    maxhamming: int = 1,
    decimate: float = 2.0,
    blur: float = 0.0,
    refine_edges: bool = True,
    debug: bool = False,
    new_param: str = ''  # 添加新参数
) -> None:
```

## 手动生成 Stub

如果需要手动生成类型存根（不通过构建流程）：

```bash
# 直接运行生成脚本
python generate_stubs.py
```

这会在项目根目录创建/更新 `apriltag.pyi` 文件。

## 开发工作流

### 本地开发

```bash
# 1. 构建并安装（会自动生成 stub）
pip install -e .

# 2. 验证 stub 文件已生成
ls -la apriltag.pyi py.typed

# 3. 测试类型检查
mypy examples/type_checking_example.py
```

### 构建分发包

```bash
# 构建源码包（会自动生成 stub）
python -m build --sdist

# 检查生成的包内容
tar -tzf dist/apriltag-python-*.tar.gz | grep -E '\.pyi|py\.typed'
```

应该看到：
```
apriltag-python-3.4.5/apriltag.pyi
apriltag-python-3.4.5/py.typed
apriltag-python-3.4.5/generate_stubs.py
```

## CI/CD 集成

GitHub Actions 会在每次构建时自动生成 stub：

```yaml
- name: Build package
  run: |
    pip install -v .  # 自动运行 generate_stubs.py

- name: Check stub files
  run: |
    ls -la apriltag.pyi py.typed
    python -c "import os; assert os.path.exists('apriltag.pyi')"
```

## 高级用法：从 C 源码提取

未来可以增强 `generate_stubs.py` 从 C 源码中提取更多信息：

### 1. 解析 docstring 文件

```python
def extract_docstrings():
    """从 .docstring 文件中提取文档。"""
    docstring_path = Path('apritag/apriltag_detect.docstring')

    if docstring_path.exists():
        with open(docstring_path) as f:
            return f.read()
```

### 2. 解析 C 头文件

```python
def parse_c_header():
    """从 apriltag.h 中提取函数签名。"""
    import re

    header_path = Path('apritag/apriltag.h')

    with open(header_path) as f:
        content = f.read()

    # 查找函数声明
    pattern = r'(\w+\s+\w+)\s*\((.*?)\);'
    matches = re.findall(pattern, content, re.MULTILINE)
```

### 3. 使用 pybind11-stubgen

对于复杂的 C++ 绑定，可以使用专门工具：

```bash
pip install pybind11-stubgen

# 生成 stub
pybind11-stubgen apriltag -o stubs/
```

## 故障排除

### Stub 文件未生成

检查构建日志：
```bash
pip install -v . 2>&1 | grep -i "stub"
```

应该看到：
```
Generating type stubs...
✓ Successfully generated stub file: /path/to/apriltag.pyi
```

### 类型检查失败

1. 确认 stub 文件存在：
   ```bash
   python -c "import apriltag, os; print(os.path.dirname(apriltag.__file__))"
   ls -la <上面的路径>/*.pyi
   ```

2. 验证 py.typed 文件：
   ```bash
   python -c "import apriltag, os; \
              stub_dir = os.path.dirname(apriltag.__file__); \
              print('py.typed exists:', os.path.exists(os.path.join(stub_dir, 'py.typed')))"
   ```

3. 测试 mypy：
   ```bash
   mypy --show-traceback examples/type_checking_example.py
   ```

### IDE 不显示类型提示

1. 重启 IDE
2. 清除 IDE 缓存
3. 重新安装包：
   ```bash
   pip uninstall apriltag-python
   pip install -e .
   ```

## 最佳实践

1. **不要手动编辑 apriltag.pyi** - 总是通过修改 `generate_stubs.py` 来更新
2. **版本控制** - 可以选择是否将生成的 `.pyi` 提交到 git
   - 提交：确保用户在不构建的情况下也能看到类型
   - 不提交：保持仓库干净，总是生成最新版本
3. **测试** - 每次修改 stub 生成逻辑后运行类型检查测试
4. **文档同步** - 保持 stub 中的文档与 README 一致

## 参考资料

- [PEP 561 - Distributing and Packaging Type Information](https://www.python.org/dev/peps/pep-0561/)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [mypy - Stub Files](https://mypy.readthedocs.io/en/stable/stubs.html)
- [pybind11-stubgen](https://github.com/sizmailov/pybind11-stubgen)
