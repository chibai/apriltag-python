# 快速开始指南

## 本地开发和测试

### 1. 克隆仓库 (如果还没有)

```bash
git clone --recursive <your-repo-url>
cd apriltag-python
```

**注意**: 必须使用 `--recursive` 来获取 apritag 子模块!

### 2. 检查子模块

```bash
# 如果之前忘记了 --recursive,可以这样获取子模块
git submodule update --init --recursive

# 验证 apritag 目录有内容
ls apritag/
```

应该能看到 apriltag.h, apriltag.c 等文件。

### 3. 创建虚拟环境 (推荐)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 4. 安装依赖

```bash
pip install --upgrade pip
pip install numpy setuptools wheel build twine
```

### 5. 本地安装 (开发模式)

```bash
# 从源码安装
pip install -e .
```

`-e` 参数表示"可编辑"模式,代码更改会立即生效。

### 6. 测试安装

```bash
# 运行测试脚本
python test_install.py
```

如果所有测试通过,说明安装成功!

### 7. 运行示例

```bash
# 需要先准备一张包含 AprilTag 的图片
# 可以从这里下载测试图片: https://github.com/AprilRobotics/apriltag-imgs

# 检测标签
python examples/detect_tags.py <image_path>

# 可视化检测结果 (需要安装 OpenCV)
pip install opencv-python
python examples/visualize_detections.py <image_path>

# 实时检测 (需要摄像头)
python examples/webcam_demo.py
```

## 构建分发包

### 构建源码包

```bash
# 清理之前的构建
rm -rf build/ dist/ *.egg-info

# 构建
python -m build --sdist

# 检查生成的包
ls dist/
```

### 测试本地构建的包

```bash
# 创建新的虚拟环境测试
python -m venv test_env
source test_env/bin/activate

# 从构建的包安装
pip install dist/apriltag-python-*.tar.gz

# 测试
python -c "import apriltag; print('OK')"
python test_install.py

# 清理
deactivate
rm -rf test_env
```

## 上传到 PyPI

详细说明请参考 [PYPI_RELEASE.md](PYPI_RELEASE.md)

### 快速流程

```bash
# 1. 先上传到 Test PyPI 测试
python -m twine upload --repository testpypi dist/*

# 2. 测试安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ apriltag-python

# 3. 确认无误后上传到正式 PyPI
python -m twine upload dist/*
```

## 开发流程

### 修改 C 代码后

如果修改了 `apritag/` 目录下的 C 源码:

```bash
# 重新构建
pip install -e . --force-reinstall --no-deps

# 或者
rm -rf build/
pip install -e .
```

### 更新文档

修改 README.md 或其他文档后,重新构建包以包含更新:

```bash
python -m build --sdist
```

### 版本发布

1. 更新版本号:
   - `setup.py`
   - `pyproject.toml`
   - `apritag/CMakeLists.txt`

2. 创建 git tag:
   ```bash
   git tag -a v3.4.5 -m "Release 3.4.5"
   git push origin v3.4.5
   ```

3. 构建并发布

## 常见问题

### Q: ImportError: No module named 'apriltag'

**A**: 确保:
1. 已激活正确的虚拟环境
2. 运行了 `pip install -e .`
3. 构建过程没有错误

### Q: CMake 相关错误

**A**:
```bash
# 检查 CMake 版本
cmake --version  # 需要 >= 3.16

# Ubuntu/Debian
sudo apt-get install cmake

# macOS
brew install cmake

# Windows
# 从 https://cmake.org/download/ 下载安装
```

### Q: NumPy 相关错误

**A**:
```bash
pip install --upgrade numpy
```

### Q: 构建很慢

**A**: 编译 C 代码需要时间,特别是首次构建。可以:
- 使用 `-j` 参数并行编译 (已在 setup.py 中配置)
- 使用更快的编译器 (如 clang)

## 项目结构

```
apriltag-python/
├── apritag/              # AprilTag C 库 (git submodule)
│   ├── apriltag.h
│   ├── apriltag.c
│   ├── apriltag_pywrap.c  # Python wrapper
│   └── ...
├── examples/             # Python 示例
│   ├── detect_tags.py
│   ├── visualize_detections.py
│   └── webcam_demo.py
├── .github/
│   └── workflows/        # CI/CD 配置
├── setup.py              # 构建脚本
├── pyproject.toml        # 现代 Python 项目配置
├── MANIFEST.in           # 指定要包含的文件
├── README.md             # 用户文档
├── PYPI_RELEASE.md       # PyPI 发布指南
├── QUICKSTART.md         # 本文件
├── test_install.py       # 安装测试脚本
└── LICENSE
```

## 有用的命令

```bash
# 查看已安装的包信息
pip show apriltag-python

# 查看包内容
pip show -f apriltag-python

# 卸载
pip uninstall apriltag-python

# 清理构建文件
rm -rf build/ dist/ *.egg-info
find . -type d -name __pycache__ -exec rm -rf {} +

# 检查包的元数据
python -m build --sdist
tar -tzf dist/apriltag-python-*.tar.gz | head -20
```

## 下一步

- 阅读 [README.md](README.md) 了解如何使用
- 查看 [examples/](examples/) 目录的示例代码
- 阅读 [PYPI_RELEASE.md](PYPI_RELEASE.md) 了解如何发布到 PyPI
- 参考 AprilTag 官方文档: https://github.com/AprilRobotics/apriltag
