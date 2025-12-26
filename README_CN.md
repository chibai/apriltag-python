# apriltag-python

[AprilTag](https://april.eecs.umich.edu/software/apriltag) 视觉基准标记检测器的 Python 包装器。

[English](README.md) | 简体中文

AprilTag 是机器人研究中流行的视觉基准标记系统。本包为 AprilTag C 库提供 Python 绑定，使得在 Python 中检测 AprilTag 变得简单。

## 特性

- 快速的 C 实现配合 Python 接口
- 支持多种标签族（tag36h11, tag36h10, tag25h9, tag16h5, tagCircle21h7, tagCircle49h12, tagStandard41h12, tagStandard52h13, tagCustom48h12）
- 多线程检测
- 可配置的检测器参数
- NumPy 集成，实现高效图像处理

## 安装

### 从 PyPI 安装

```bash
pip install apriltag-python
```

### 从源码安装

要求：
- CMake >= 3.16
- Python >= 3.10
- NumPy >= 1.17.0
- C 编译器（gcc、clang 或 MSVC）

```bash
git clone --recursive https://github.com/chibai/apriltag-python.git
cd apriltag-python
pip install .
```

**注意**：必须使用 `--recursive` 标志来克隆 AprilTag C 库子模块。

## 快速开始

```python
import apriltag
import cv2

# 加载图像
image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# 创建 AprilTag 检测器
detector = apriltag.apriltag(
    family='tag36h11',      # 标签族
    threads=4,              # 线程数
    maxhamming=1,           # 最大汉明距离
    decimate=2.0,           # 降采样因子
    blur=0.0,               # 高斯模糊
    refine_edges=True,      # 优化边缘
    debug=False             # 调试模式
)

# 检测标签
detections = detector.detect(image)

# 处理检测结果
for detection in detections:
    print(f"标签 ID: {detection['id']}")
    print(f"中心点: {detection['center']}")
    print(f"角点: {detection['lb-rb-rt-lt']}")
    print(f"汉明距离: {detection['hamming']}")
    print(f"决策边界: {detection['margin']}")
```

## API 参考

### 创建检测器

```python
detector = apriltag.apriltag(
    family,           # 标签族名称（必需）
    threads=1,        # 检测线程数
    maxhamming=1,     # 可纠正的最大位错误数
    decimate=2.0,     # 检测分辨率降采样因子
    blur=0.0,         # 高斯模糊标准差（0 = 无模糊）
    refine_edges=True,# 优化四边形边缘
    debug=False       # 启用调试输出
)
```

#### 参数说明

- **family**（字符串，必需）：标签族名称。选项：
  - `'tag36h11'` - 推荐，36位标签，最小汉明距离为11
  - `'tag36h10'` - 36位标签，最小汉明距离为10
  - `'tag25h9'` - 25位标签，最小汉明距离为9
  - `'tag16h5'` - 16位标签，最小汉明距离为5
  - `'tagCircle21h7'` - 圆形标签
  - `'tagCircle49h12'` - 圆形标签
  - `'tagStandard41h12'` - 标准标签
  - `'tagStandard52h13'` - 标准标签
  - `'tagCustom48h12'` - 自定义标签

- **threads**（整数，默认=1）：用于检测的线程数。设置为 CPU 核心数可获得最佳性能。

- **maxhamming**（整数，默认=1）：可纠正的最大位错误数。较高的值允许检测更多损坏的标签，但会增加误检率。范围：0-3。

- **decimate**（浮点数，默认=2.0）：在降低分辨率的图像上执行检测。较高的值提高速度但降低精度。设置为1.0以获得全分辨率。

- **blur**（浮点数，默认=0.0）：高斯模糊标准差（像素）。可以帮助处理噪声图像。

- **refine_edges**（布尔值，默认=True）：优化四边形边缘位置以提高精度。建议保持启用。

- **debug**（布尔值，默认=False）：启用调试输出并保存中间图像。

### 检测

```python
detections = detector.detect(image)
```

#### 参数

- **image**（numpy.ndarray）：灰度图像，2D NumPy 数组，uint8 类型。

#### 返回值

检测字典的元组，每个包含：

- **id**（整数）：解码的标签 ID
- **hamming**（整数）：纠正的错误位数
- **margin**（浮点数）：决策边界（越高越好，检测质量的度量）
- **center**（numpy.ndarray）：标签中心坐标 [x, y]
- **lb-rb-rt-lt**（numpy.ndarray）：4x2 角点坐标数组，顺序：左下、右下、右上、左上

## 示例：绘制检测结果

```python
import apriltag
import cv2
import numpy as np

# 加载图像
image = cv2.imread('tags.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 创建检测器
detector = apriltag.apriltag('tag36h11', threads=4)

# 检测
detections = detector.detect(gray)

# 绘制结果
for detection in detections:
    # 绘制角点
    corners = detection['lb-rb-rt-lt'].astype(int)
    for i in range(4):
        pt1 = tuple(corners[i])
        pt2 = tuple(corners[(i + 1) % 4])
        cv2.line(image, pt1, pt2, (0, 255, 0), 2)

    # 绘制中心点
    center = tuple(detection['center'].astype(int))
    cv2.circle(image, center, 5, (0, 0, 255), -1)

    # 绘制 ID
    cv2.putText(image, str(detection['id']), center,
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

cv2.imshow('检测结果', image)
cv2.waitKey(0)
```

## 性能优化建议

1. **使用多线程**：将 `threads` 设置为 CPU 核心数以实现并行处理
2. **调整降采样**：对于较大的标签，增加 `decimate` 以加快检测速度
3. **选择合适的标签族**：tag36h11 在速度和鲁棒性之间提供了良好的平衡
4. **降低 maxhamming**：较低的值更快，但对损坏标签的容忍度较低

## 标签生成

可以使用官方 AprilTag 工具或在线生成器生成 AprilTag 图像：

- [官方 AprilTag 生成器](https://github.com/AprilRobotics/apriltag-generation)
- AprilTag 仓库中提供预生成的 PDF

## 许可证

本包封装了 AprilTag C 库，该库采用 BSD 2-Clause 许可证。详见 [LICENSE](LICENSE)。

## 引用

如果您在研究中使用 AprilTag，请引用：

```
@inproceedings{wang2016iros,
  author = {John Wang and Edwin Olson},
  title = {{AprilTag 2}: Efficient and robust fiducial detection},
  booktitle = {Proceedings of the {IEEE/RSJ} International Conference on Intelligent
  Robots and Systems {(IROS)}},
  year = {2016},
  month = {October}
}
```

## 关于本项目

本项目为 [AprilTag C 库](https://github.com/AprilRobotics/apriltag)提供 Python 绑定。它独立于原始 AprilTag 项目进行维护。

- **Python 绑定仓库**：https://github.com/chibai/apriltag-python
- **原始 AprilTag C 库**：https://github.com/AprilRobotics/apriltag
- **AprilTag 官方网站**：https://april.eecs.umich.edu/software/apriltag

## 贡献

欢迎在 [GitHub 仓库](https://github.com/chibai/apriltag-python)提交错误报告和拉取请求。

对于 AprilTag 算法或 C 库相关的问题，请参考[官方 AprilTag 仓库](https://github.com/AprilRobotics/apriltag)。

## 致谢

- AprilTag 由密歇根大学 April Robotics Lab 开发
- 本 Python 绑定由 chibai 和贡献者维护
