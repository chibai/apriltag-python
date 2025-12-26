#!/usr/bin/env python3
"""
Simple test script to verify apriltag installation.
"""

import sys
import numpy as np


def test_import():
    """Test if apriltag module can be imported."""
    print("Testing apriltag import...")
    try:
        import apriltag
        print("✓ apriltag module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import apriltag: {e}")
        return False


def test_detector_creation():
    """Test if detector can be created."""
    print("\nTesting detector creation...")
    try:
        import apriltag

        # Test all supported tag families
        families = [
            'tag36h11', 'tag36h10', 'tag25h9', 'tag16h5',
            'tagCircle21h7', 'tagCircle49h12',
            'tagStandard41h12', 'tagStandard52h13',
            'tagCustom48h12'
        ]

        for family in families:
            detector = apriltag.apriltag(family)
            print(f"  ✓ Created detector with family: {family}")

        print("✓ All detector families work")
        return True
    except Exception as e:
        print(f"✗ Failed to create detector: {e}")
        return False


def test_detection():
    """Test detection on a synthetic image."""
    print("\nTesting detection on synthetic image...")
    try:
        import apriltag

        # Create a blank test image
        test_image = np.zeros((480, 640), dtype=np.uint8)

        # Create detector
        detector = apriltag.apriltag('tag36h11', threads=1)

        # Run detection (should return empty tuple on blank image)
        detections = detector.detect(test_image)

        print(f"  Detection returned {len(detections)} tags (expected 0 for blank image)")
        print("✓ Detection function works")
        return True
    except Exception as e:
        print(f"✗ Detection failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_detector_parameters():
    """Test detector with various parameters."""
    print("\nTesting detector parameters...")
    try:
        import apriltag

        detector = apriltag.apriltag(
            family='tag36h11',
            threads=2,
            maxhamming=2,
            decimate=1.0,
            blur=0.5,
            refine_edges=False,
            debug=False
        )

        print("✓ Detector created with custom parameters")
        return True
    except Exception as e:
        print(f"✗ Failed with custom parameters: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("AprilTag Python Installation Test")
    print("=" * 60)

    tests = [
        test_import,
        test_detector_creation,
        test_detection,
        test_detector_parameters,
    ]

    results = []
    for test in tests:
        results.append(test())

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✓ All tests passed!")
        print("\nYou can now use apriltag-python. Try:")
        print("  python examples/detect_tags.py <image_path>")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
