# 类型提示支持

apriltag-python 包含完整的类型提示（Type Hints）支持，可以与 IDE 和静态类型检查工具（如 mypy）无缝集成。

## 特性

- ✅ 完整的 `.pyi` 存根文件
- ✅ `py.typed` 标记文件（PEP 561 兼容）
- ✅ 支持 mypy、Pylance、Pyright 等类型检查器
- ✅ IDE 自动补全和类型提示
- ✅ Python 3.10+ 的现代类型语法

## 使用示例

### 基础类型提示

```python
import apriltag
import numpy as np
import numpy.typing as npt

# 创建检测器 - IDE 会提示所有参数
detector: apriltag.apriltag = apriltag.apriltag(
    family='tag36h11',  # IDE 会自动补全可用的 tag family
    threads=4,
    maxhamming=1
)

# 检测 - 返回类型是 tuple[Detection, ...]
image: npt.NDArray[np.uint8] = np.zeros((480, 640), dtype=np.uint8)
detections: tuple[apriltag.Detection, ...] = detector.detect(image)

# 处理检测结果 - IDE 知道 Detection 的结构
for detection in detections:
    tag_id: int = detection['id']
    center: npt.NDArray[np.float64] = detection['center']
    corners: npt.NDArray[np.float64] = detection['lb-rb-rt-lt']
```

### 使用 TypedDict

```python
from apriltag import Detection

def process_detection(det: Detection) -> None:
    # IDE 会提示可用的键
    print(f"Tag ID: {det['id']}")           # int
    print(f"Hamming: {det['hamming']}")     # int
    print(f"Margin: {det['margin']}")       # float
    print(f"Center: {det['center']}")       # NDArray[float64]
    print(f"Corners: {det['lb-rb-rt-lt']}") # NDArray[float64]
```

### Tag Family 类型

```python
from apriltag import TagFamily

# 使用 Literal 类型确保只能使用有效的 tag family
def create_detector(family: TagFamily) -> apriltag.apriltag:
    return apriltag.apriltag(family)

# IDE 会检查这些调用
detector1 = create_detector('tag36h11')  # ✓ 正确
detector2 = create_detector('invalid')   # ✗ 类型错误
```

## 静态类型检查

### 使用 mypy

安装 mypy：
```bash
pip install mypy
```

检查代码：
```bash
mypy your_script.py
```

### mypy 配置示例

创建 `mypy.ini` 或在 `pyproject.toml` 中添加：

```ini
[mypy]
python_version = 3.10
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

[mypy-cv2.*]
ignore_missing_imports = True
```

或在 `pyproject.toml` 中：

```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "cv2.*"
ignore_missing_imports = true
```

### 示例代码检查

```python
# good_example.py
import apriltag
import numpy as np

def detect_tags(image: np.ndarray) -> tuple[apriltag.Detection, ...]:
    detector = apriltag.apriltag('tag36h11')
    return detector.detect(image)

# mypy good_example.py
# Success: no issues found
```

```python
# bad_example.py
import apriltag

def detect_tags(image):  # 缺少类型提示
    detector = apriltag.apriltag('invalid_family')  # 无效的 family
    return detector.detect(image)

# mypy bad_example.py
# error: Argument 1 to "apriltag" has incompatible type "str"; expected "Literal['tag36h11', ...]"
```

## IDE 支持

### VSCode

安装 Pylance 扩展后，自动获得：
- 参数提示
- 自动补全
- 类型检查
- 跳转到定义

### PyCharm

PyCharm Professional 自动识别 `.pyi` 文件，提供：
- 智能补全
- 类型检查
- 快速文档
- 重构支持

### Vim/Neovim

使用 coc.nvim 或 ALE 配合 Pyright：
```vim
" 在 .vimrc 或 init.vim 中
Plug 'neoclide/coc.nvim', {'branch': 'release'}
```

## 完整示例

参见 [examples/type_checking_example.py](examples/type_checking_example.py) 查看完整的类型提示使用示例。

运行示例：
```bash
# 运行脚本
python examples/type_checking_example.py image.jpg

# 类型检查
mypy examples/type_checking_example.py
```

## 类型定义参考

### apriltag.apriltag

```python
class apriltag:
    def __init__(
        self,
        family: TagFamily,
        threads: int = 1,
        maxhamming: int = 1,
        decimate: float = 2.0,
        blur: float = 0.0,
        refine_edges: bool = True,
        debug: bool = False
    ) -> None: ...

    def detect(
        self,
        image: npt.NDArray[np.uint8]
    ) -> tuple[Detection, ...]: ...
```

### Detection TypedDict

```python
class Detection(TypedDict):
    id: int
    hamming: int
    margin: float
    center: npt.NDArray[np.float64]  # Shape: (2,)
    # 'lb-rb-rt-lt': npt.NDArray[np.float64]  # Shape: (4, 2)
```

注意：由于 `lb-rb-rt-lt` 包含连字符，在代码中只能使用字典访问方式：
```python
corners = detection['lb-rb-rt-lt']  # 正确
# corners = detection.lb-rb-rt-lt   # 语法错误
```

### TagFamily Literal

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
    'tagCustom48h12'
]
```

## 常见问题

### Q: 为什么 IDE 没有显示类型提示？

A: 确保：
1. 包已正确安装：`pip install apriltag-python`
2. `.pyi` 文件已安装：检查 `site-packages/` 目录
3. IDE 已重启或重新加载项目

### Q: mypy 报告找不到类型存根？

A: 检查 `py.typed` 文件是否存在：
```bash
python -c "import apriltag; import os; print(os.path.dirname(apriltag.__file__))"
# 检查该目录下是否有 py.typed 和 apriltag.pyi
```

### Q: 如何处理 OpenCV 的类型问题？

A: OpenCV 没有完整的类型存根。在 mypy 配置中忽略它：
```ini
[mypy-cv2.*]
ignore_missing_imports = True
```

或使用类型注释：
```python
import cv2
from typing import Any

image: Any = cv2.imread('image.jpg')
```

## 参考资料

- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [PEP 561 - Distributing and Packaging Type Information](https://www.python.org/dev/peps/pep-0561/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [typing module](https://docs.python.org/3/library/typing.html)
