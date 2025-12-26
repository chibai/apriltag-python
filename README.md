# apriltag-python

A Python wrapper for the [AprilTag](https://april.eecs.umich.edu/software/apriltag) visual fiducial detector.

AprilTag is a visual fiducial system popular in robotics research. This package provides Python bindings for the AprilTag C library, making it easy to detect AprilTags in images from Python.

## Features

- Fast C implementation with Python interface
- Support for multiple tag families (tag36h11, tag36h10, tag25h9, tag16h5, tagCircle21h7, tagCircle49h12, tagStandard41h12, tagStandard52h13, tagCustom48h12)
- Multi-threaded detection
- Configurable detector parameters
- NumPy integration for efficient image processing

## Installation

### From PyPI

```bash
pip install apriltag-python
```

### From Source

Requirements:
- CMake >= 3.16
- Python >= 3.10
- NumPy >= 1.17.0
- C compiler (gcc, clang, or MSVC)

```bash
git clone --recursive https://github.com/chibai/apriltag-python.git
cd apriltag-python
pip install .
```

**Note**: The `--recursive` flag is important to clone the AprilTag C library submodule.

## Quick Start

```python
import apriltag
import cv2

# Load an image
image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Create an AprilTag detector
detector = apriltag.apriltag(
    family='tag36h11',
    threads=4,
    maxhamming=1,
    decimate=2.0,
    blur=0.0,
    refine_edges=True,
    debug=False
)

# Detect tags
detections = detector.detect(image)

# Process detections
for detection in detections:
    print(f"Tag ID: {detection['id']}")
    print(f"Center: {detection['center']}")
    print(f"Corners: {detection['lb-rb-rt-lt']}")
    print(f"Hamming distance: {detection['hamming']}")
    print(f"Decision margin: {detection['margin']}")
```

## API Reference

### Detector Creation

```python
detector = apriltag.apriltag(
    family,           # Tag family name (required)
    threads=1,        # Number of threads for detection
    maxhamming=1,     # Maximum number of bit errors to correct
    decimate=2.0,     # Detection resolution downsampling factor
    blur=0.0,         # Gaussian blur sigma (0 = no blur)
    refine_edges=True,# Refine quad edges
    debug=False       # Enable debug output
)
```

#### Parameters

- **family** (str, required): Tag family name. Options:
  - `'tag36h11'` - Recommended, 36-bit tags with min. Hamming distance of 11
  - `'tag36h10'` - 36-bit tags with min. Hamming distance of 10
  - `'tag25h9'` - 25-bit tags with min. Hamming distance of 9
  - `'tag16h5'` - 16-bit tags with min. Hamming distance of 5
  - `'tagCircle21h7'` - Circular tags
  - `'tagCircle49h12'` - Circular tags
  - `'tagStandard41h12'` - Standard tags
  - `'tagStandard52h13'` - Standard tags
  - `'tagCustom48h12'` - Custom tags

- **threads** (int, default=1): Number of threads to use for detection. Set to number of CPU cores for best performance.

- **maxhamming** (int, default=1): Maximum number of bit errors that can be corrected. Higher values allow detection of more damaged tags but increase false positive rate. Range: 0-3.

- **decimate** (float, default=2.0): Detection is performed on a reduced-resolution image. Higher values increase speed but reduce accuracy. Set to 1.0 for full resolution.

- **blur** (float, default=0.0): Gaussian blur standard deviation in pixels. Can help with noisy images.

- **refine_edges** (bool, default=True): Refine quad edge positions for better accuracy. Recommended to keep enabled.

- **debug** (bool, default=False): Enable debug output and save intermediate images.

### Detection

```python
detections = detector.detect(image)
```

#### Parameters

- **image** (numpy.ndarray): Grayscale image as a 2D NumPy array of uint8 values.

#### Returns

A tuple of detection dictionaries, each containing:

- **id** (int): The decoded tag ID
- **hamming** (int): Number of error bits corrected
- **margin** (float): Decision margin (higher is better, measure of detection quality)
- **center** (numpy.ndarray): Tag center coordinates [x, y]
- **lb-rb-rt-lt** (numpy.ndarray): 4x2 array of corner coordinates in order: left-bottom, right-bottom, right-top, left-top

## Example: Drawing Detections

```python
import apriltag
import cv2
import numpy as np

# Load image
image = cv2.imread('tags.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Create detector
detector = apriltag.apriltag('tag36h11', threads=4)

# Detect
detections = detector.detect(gray)

# Draw results
for detection in detections:
    # Draw corners
    corners = detection['lb-rb-rt-lt'].astype(int)
    for i in range(4):
        pt1 = tuple(corners[i])
        pt2 = tuple(corners[(i + 1) % 4])
        cv2.line(image, pt1, pt2, (0, 255, 0), 2)

    # Draw center
    center = tuple(detection['center'].astype(int))
    cv2.circle(image, center, 5, (0, 0, 255), -1)

    # Draw ID
    cv2.putText(image, str(detection['id']), center,
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

cv2.imshow('Detections', image)
cv2.waitKey(0)
```

## Performance Tips

1. **Use multiple threads**: Set `threads` to the number of CPU cores for parallel processing
2. **Adjust decimation**: Increase `decimate` for faster detection of larger tags
3. **Choose appropriate tag family**: tag36h11 provides good balance of speed and robustness
4. **Reduce maxhamming**: Lower values are faster but less tolerant of damaged tags

## Tag Generation

AprilTag images can be generated using the official AprilTag tools or online generators:

- [Official AprilTag Generator](https://github.com/AprilRobotics/apriltag-generation)
- Pre-generated PDFs available in the AprilTag repository

## License

This package wraps the AprilTag C library, which is licensed under the BSD 2-Clause License. See [LICENSE](LICENSE) for details.

## Citation

If you use AprilTag in your research, please cite:

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

## About This Project

This project provides Python bindings for the [AprilTag C library](https://github.com/AprilRobotics/apriltag). It is maintained independently from the original AprilTag project.

- **Python Bindings Repository**: https://github.com/chibai/apriltag-python
- **Original AprilTag C Library**: https://github.com/AprilRobotics/apriltag
- **AprilTag Official Website**: https://april.eecs.umich.edu/software/apriltag

## Contributing

Bug reports and pull requests are welcome on the [GitHub repository](https://github.com/chibai/apriltag-python).

For issues specific to the AprilTag algorithm or C library, please refer to the [official AprilTag repository](https://github.com/AprilRobotics/apriltag).

## Acknowledgments

- AprilTag was developed by the April Robotics Lab at the University of Michigan
- This Python binding is maintained by chibai and contributors
