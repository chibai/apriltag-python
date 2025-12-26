#!/usr/bin/env python3
"""
Simple AprilTag detection example.
Detects AprilTags in an image and prints detection information.
"""

import apriltag
import cv2
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python detect_tags.py <image_path> [tag_family]")
        print("Example: python detect_tags.py image.jpg tag36h11")
        sys.exit(1)

    image_path = sys.argv[1]
    tag_family = sys.argv[2] if len(sys.argv) > 2 else 'tag36h11'

    # Load image
    print(f"Loading image: {image_path}")
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print(f"Error: Could not load image from {image_path}")
        sys.exit(1)

    print(f"Image size: {image.shape[1]}x{image.shape[0]}")

    # Create detector
    print(f"Creating detector with tag family: {tag_family}")
    detector = apriltag.apriltag(
        family=tag_family,
        threads=4,
        maxhamming=1,
        decimate=2.0,
        blur=0.0,
        refine_edges=True,
        debug=False
    )

    # Detect tags
    print("Detecting tags...")
    detections = detector.detect(image)

    print(f"\nFound {len(detections)} tag(s)")
    print("-" * 60)

    # Print detection details
    for i, detection in enumerate(detections):
        print(f"\nTag {i + 1}:")
        print(f"  ID: {detection['id']}")
        print(f"  Hamming: {detection['hamming']}")
        print(f"  Decision Margin: {detection['margin']:.2f}")
        print(f"  Center: ({detection['center'][0]:.1f}, {detection['center'][1]:.1f})")
        print(f"  Corners:")
        corners = detection['lb-rb-rt-lt']
        corner_names = ['Left-Bottom', 'Right-Bottom', 'Right-Top', 'Left-Top']
        for j, name in enumerate(corner_names):
            print(f"    {name}: ({corners[j][0]:.1f}, {corners[j][1]:.1f})")


if __name__ == '__main__':
    main()
