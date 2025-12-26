#!/usr/bin/env python3
"""
Example demonstrating type checking with apriltag-python.

This example shows how to use the apriltag module with proper type hints
for better IDE support and static type checking with mypy.
"""

import apriltag
import numpy as np
import numpy.typing as npt


def detect_tags_with_types(
    image_path: str,
    family: apriltag.TagFamily = 'tag36h11'
) -> tuple[apriltag.Detection, ...]:
    """
    Detect AprilTags in an image with full type hints.

    Args:
        image_path: Path to the image file
        family: Tag family to use for detection

    Returns:
        Tuple of detections with type hints

    Example:
        >>> detections = detect_tags_with_types('image.jpg', 'tag36h11')
        >>> for det in detections:
        ...     print(f"Tag {det['id']} at {det['center']}")
    """
    import cv2

    # Load image (cv2.imread returns np.ndarray | None)
    image: npt.NDArray[np.uint8] | None = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    # Create detector with type hints
    detector: apriltag.apriltag = apriltag.apriltag(
        family=family,
        threads=4,
        maxhamming=1,
        decimate=2.0,
        blur=0.0,
        refine_edges=True,
        debug=False
    )

    # Detect tags
    detections: tuple[apriltag.Detection, ...] = detector.detect(image)

    return detections


def process_detection(detection: apriltag.Detection) -> dict[str, float]:
    """
    Process a single detection and extract information.

    Args:
        detection: AprilTag detection dictionary

    Returns:
        Dictionary with processed information
    """
    # Type checker knows the structure of Detection
    tag_id: int = detection['id']
    hamming: int = detection['hamming']
    margin: float = detection['margin']
    center: npt.NDArray[np.float64] = detection['center']
    corners: npt.NDArray[np.float64] = detection['lb-rb-rt-lt']

    # Calculate tag area
    p1, p2, p3, p4 = corners
    area: float = 0.5 * abs(
        (p1[0] * p2[1] - p2[0] * p1[1]) +
        (p2[0] * p3[1] - p3[0] * p2[1]) +
        (p3[0] * p4[1] - p4[0] * p3[1]) +
        (p4[0] * p1[1] - p1[0] * p4[1])
    )

    return {
        'id': float(tag_id),
        'quality': margin,
        'center_x': center[0],
        'center_y': center[1],
        'area': area
    }


def main() -> None:
    """Main function with type hints."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python type_checking_example.py <image_path>")
        sys.exit(1)

    image_path: str = sys.argv[1]

    try:
        detections = detect_tags_with_types(image_path)

        print(f"Found {len(detections)} tag(s)\n")

        for i, detection in enumerate(detections):
            info = process_detection(detection)
            print(f"Tag {i + 1}:")
            print(f"  ID: {int(info['id'])}")
            print(f"  Quality: {info['quality']:.2f}")
            print(f"  Center: ({info['center_x']:.1f}, {info['center_y']:.1f})")
            print(f"  Area: {info['area']:.1f} px²")
            print()

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
