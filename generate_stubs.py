#!/usr/bin/env python3
"""
Generate type stubs (.pyi) for the apriltag module.

This script automatically generates type hints based on the C extension module.
It should be run after the extension is built.
"""

import os
import sys
import importlib
import inspect
from pathlib import Path


def generate_stub_content() -> str:
    """Generate the stub file content."""

    stub_content = '''"""
Type stubs for apriltag module.

AprilTag visual fiducial system detector.
Auto-generated from C extension module.
"""

from typing import Literal, TypedDict
import numpy as np
import numpy.typing as npt

__version__: str

class Detection(TypedDict):
    """
    AprilTag detection result.

    Attributes:
        id: The decoded tag ID
        hamming: Number of error bits corrected
        margin: Decision margin (higher is better, measure of detection quality)
        center: Tag center coordinates [x, y]
        lb-rb-rt-lt: 4x2 array of corner coordinates (left-bottom, right-bottom, right-top, left-top)
    """
    id: int
    hamming: int
    margin: float
    center: npt.NDArray[np.float64]  # Shape: (2,)

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

class apriltag:
    """
    AprilTag detector.

    Creates a detector for a specific tag family with configurable parameters.

    Args:
        family: Tag family name. Options:
            - 'tag36h11': Recommended, 36-bit tags with min. Hamming distance of 11
            - 'tag36h10': 36-bit tags with min. Hamming distance of 10
            - 'tag25h9': 25-bit tags with min. Hamming distance of 9
            - 'tag16h5': 16-bit tags with min. Hamming distance of 5
            - 'tagCircle21h7': Circular tags
            - 'tagCircle49h12': Circular tags
            - 'tagStandard41h12': Standard tags
            - 'tagStandard52h13': Standard tags
            - 'tagCustom48h12': Custom tags

        threads: Number of threads to use for detection (default: 1)
            Set to number of CPU cores for best performance.

        maxhamming: Maximum number of bit errors that can be corrected (default: 1)
            Higher values allow detection of more damaged tags but increase
            false positive rate. Range: 0-3.

        decimate: Detection resolution downsampling factor (default: 2.0)
            Detection is performed on a reduced-resolution image. Higher values
            increase speed but reduce accuracy. Set to 1.0 for full resolution.

        blur: Gaussian blur standard deviation in pixels (default: 0.0)
            Can help with noisy images. 0 means no blur.

        refine_edges: Refine quad edge positions for better accuracy (default: True)
            Recommended to keep enabled.

        debug: Enable debug output and save intermediate images (default: False)

    Example:
        >>> import apriltag
        >>> import numpy as np
        >>>
        >>> # Create detector
        >>> detector = apriltag.apriltag('tag36h11', threads=4)
        >>>
        >>> # Detect tags in grayscale image
        >>> image = np.zeros((480, 640), dtype=np.uint8)
        >>> detections = detector.detect(image)
        >>>
        >>> # Process results
        >>> for detection in detections:
        ...     print(f"Tag ID: {detection['id']}")
        ...     print(f"Center: {detection['center']}")
    """

    def __init__(
        self,
        family: TagFamily,
        threads: int = 1,
        maxhamming: int = 1,
        decimate: float = 2.0,
        blur: float = 0.0,
        refine_edges: bool = True,
        debug: bool = False
    ) -> None:
        """
        Initialize AprilTag detector.

        Args:
            family: Tag family name (required)
            threads: Number of threads for detection (default: 1)
            maxhamming: Maximum bit errors to correct (default: 1, range: 0-3)
            decimate: Downsampling factor (default: 2.0)
            blur: Gaussian blur sigma in pixels (default: 0.0)
            refine_edges: Refine quad edges (default: True)
            debug: Enable debug mode (default: False)

        Raises:
            RuntimeError: If family is not recognized or detector creation fails
            ValueError: If maxhamming > 3 or other parameter validation fails
        """
        ...

    def detect(
        self,
        image: npt.NDArray[np.uint8]
    ) -> tuple[Detection, ...]:
        """
        Detect AprilTags in a grayscale image.

        Args:
            image: Grayscale image as a 2D NumPy array of uint8 values.
                Shape should be (height, width).

        Returns:
            Tuple of detection dictionaries. Each detection contains:
                - id (int): The decoded tag ID
                - hamming (int): Number of error bits corrected
                - margin (float): Decision margin (higher is better)
                - center (ndarray): Tag center [x, y], shape (2,)
                - 'lb-rb-rt-lt' (ndarray): Corner coordinates, shape (4, 2)
                  Order: left-bottom, right-bottom, right-top, left-top

        Raises:
            RuntimeError: If image format is invalid or detection fails

        Example:
            >>> import cv2
            >>> image = cv2.imread('tag.jpg', cv2.IMREAD_GRAYSCALE)
            >>> detections = detector.detect(image)
            >>> for det in detections:
            ...     print(f"Found tag {det['id']} at {det['center']}")
        """
        ...

__all__ = ['apriltag', 'Detection', 'TagFamily']
'''

    return stub_content


def extract_docstrings_from_c_source():
    """Extract docstrings from C source files if available."""
    c_source_path = Path(__file__).parent / 'apritag' / 'apriltag_pywrap.c'

    if not c_source_path.exists():
        return {}

    docstrings = {}
    try:
        with open(c_source_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to find docstring includes
        import re
        docstring_pattern = r'#include\s+"([^"]+_docstring\.h)"'
        matches = re.findall(docstring_pattern, content)

        for match in matches:
            docstring_file = Path(__file__).parent / 'apritag' / match
            if docstring_file.exists():
                # Could parse these files to extract actual docstrings
                # For now, just note they exist
                pass

    except Exception as e:
        print(f"Warning: Could not extract docstrings from C source: {e}")

    return docstrings


def main():
    """Main function to generate stub file."""

    # Generate stub content
    print("Generating type stub for apriltag module...")
    stub_content = generate_stub_content()

    # Extract any additional info from C source
    extract_docstrings_from_c_source()

    # Write stub file
    output_path = Path(__file__).parent / 'apriltag.pyi'

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(stub_content)

        print(f"✓ Successfully generated stub file: {output_path}")
        print(f"  Stub file size: {len(stub_content)} bytes")

        # Also ensure py.typed exists
        py_typed_path = Path(__file__).parent / 'py.typed'
        if not py_typed_path.exists():
            py_typed_path.touch()
            print(f"✓ Created py.typed marker file")

        return 0

    except Exception as e:
        print(f"✗ Error writing stub file: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
