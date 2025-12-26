# PyPI 发布指南

这份文档说明如何将 apriltag-python 包上传到 PyPI。

## 准备工作

### 1. 安装必要的工具

```bash
pip install --upgrade pip setuptools wheel twine build
```

### 2. 确保 CMake 已安装

```bash
cmake --version  # 应该 >= 3.16
```

### 3. 注册 PyPI 账号

- 主 PyPI: https://pypi.org/account/register/
- 测试 PyPI (建议先在这里测试): https://test.pypi.org/account/register/

### 4. 配置 API Token (推荐)

1. 登录 PyPI
2. 进入 Account Settings -> API tokens
3. 创建新 token (scope 可以选择整个账户或特定项目)
4. 保存 token (只会显示一次!)

创建 `~/.pypirc` 文件:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

## 构建和发布流程

### 步骤 1: 清理旧的构建文件

```bash
# 清理之前的构建产物
rm -rf build/ dist/ *.egg-info
```

### 步骤 2: 构建源码包

```bash
# 使用 build 工具构建
python -m build --sdist
```

这会在 `dist/` 目录创建一个 `.tar.gz` 文件。

### 步骤 3: 本地测试构建

```bash
# 在虚拟环境中测试安装
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# 从源码包安装
pip install dist/apriltag-python-3.4.5.tar.gz

# 测试导入
python -c "import apriltag; print('Success!')"

# 清理
deactivate
rm -rf test_env
```

### 步骤 4: 上传到 Test PyPI (推荐先测试)

```bash
# 上传到测试服务器
python -m twine upload --repository testpypi dist/*

# 测试从 Test PyPI 安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ apriltag-python
```

注意: `--extra-index-url` 是必需的,因为依赖包 (numpy) 在主 PyPI 上。

### 步骤 5: 上传到正式 PyPI

```bash
# 确认一切正常后,上传到正式 PyPI
python -m twine upload dist/*
```

### 步骤 6: 验证发布

```bash
# 等待几分钟后,从 PyPI 安装测试
pip install apriltag-python

# 测试
python -c "import apriltag; d = apriltag.apriltag('tag36h11'); print('Installation successful!')"
```

## 版本更新流程

当需要发布新版本时:

### 1. 更新版本号

需要在以下文件中更新版本号:

- `setup.py` (version 参数)
- `pyproject.toml` ([project] version)
- `apritag/CMakeLists.txt` (project VERSION)

### 2. 更新 CHANGELOG

创建或更新 CHANGELOG.md 记录变更。

### 3. 创建 Git Tag

```bash
git tag -a v3.4.5 -m "Release version 3.4.5"
git push origin v3.4.5
```

### 4. 按照上述发布流程构建和上传

## 构建二进制 Wheel (可选,高级)

为了让用户安装更快,可以构建预编译的 wheel 包:

### 使用 cibuildwheel 构建多平台 wheels

1. 安装 cibuildwheel:
```bash
pip install cibuildwheel
```

2. 构建 wheels:
```bash
# Linux wheels (需要在 Linux 上运行)
cibuildwheel --platform linux

# macOS wheels (需要在 macOS 上运行)
cibuildwheel --platform macos

# Windows wheels (需要在 Windows 上运行)
cibuildwheel --platform windows
```

3. 创建 `.github/workflows/build-wheels.yml` 使用 GitHub Actions 自动构建:

```yaml
name: Build Wheels

on: [push, pull_request]

jobs:
  build_wheels:
    name: Build wheels on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]

    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Build wheels
        uses: pypa/cibuildwheel@v2.16.0

      - uses: actions/upload-artifact@v3
        with:
          path: ./wheelhouse/*.whl
```

## 常见问题

### Q: 上传时提示 "File already exists"

A: PyPI 不允许覆盖已上传的版本。你需要:
1. 增加版本号
2. 或者删除远程的版本 (只能在发布后的几小时内)

### Q: 构建失败,找不到 CMake

A: 确保:
1. CMake 已安装: `cmake --version`
2. CMake 在 PATH 中
3. 版本 >= 3.16

### Q: 导入时出现 "No module named 'apriltag'"

A: 检查:
1. 扩展模块是否正确编译
2. NumPy 是否已安装
3. Python 版本是否兼容 (>= 3.7)

### Q: 在某些平台上安装失败

A: 可能需要:
1. 构建并上传预编译的 wheel 包
2. 或在 README 中说明该平台的额外要求

## 最佳实践

1. **始终先在 Test PyPI 测试** - 避免在正式环境出错
2. **使用 API token** - 比用户名/密码更安全
3. **版本语义化** - 遵循 semver (major.minor.patch)
4. **保持 CHANGELOG** - 让用户了解变更
5. **自动化 CI/CD** - 使用 GitHub Actions 自动构建和测试
6. **提供 wheels** - 让安装更快更容易

## 参考资料

- [PyPI 官方文档](https://packaging.python.org/)
- [Twine 文档](https://twine.readthedocs.io/)
- [setuptools 文档](https://setuptools.pypa.io/)
- [cibuildwheel 文档](https://cibuildwheel.readthedocs.io/)
