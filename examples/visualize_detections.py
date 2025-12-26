#!/usr/bin/env python3
"""
Visualize AprilTag detections.
Detects AprilTags in an image and displays them with annotations.
"""

import apriltag
import cv2
import numpy as np
import sys


def draw_detections(image, detections):
    """
    Draw detected AprilTags on the image.

    Args:
        image: BGR color image
        detections: List of detection dictionaries
    """
    output = image.copy()

    for detection in detections:
        # Get corners and convert to integer coordinates
        corners = detection['lb-rb-rt-lt'].astype(int)

        # Draw quadrilateral outline
        for i in range(4):
            pt1 = tuple(corners[i])
            pt2 = tuple(corners[(i + 1) % 4])
            cv2.line(output, pt1, pt2, (0, 255, 0), 2)

        # Draw center point
        center = tuple(detection['center'].astype(int))
        cv2.circle(output, center, 5, (0, 0, 255), -1)

        # Draw tag ID
        tag_id = str(detection['id'])
        font_scale = 0.8
        thickness = 2
        text_size = cv2.getTextSize(tag_id, cv2.FONT_HERSHEY_SIMPLEX,
                                    font_scale, thickness)[0]

        # Position text above center
        text_x = center[0] - text_size[0] // 2
        text_y = center[1] - 10

        # Draw text background
        cv2.rectangle(output,
                     (text_x - 5, text_y - text_size[1] - 5),
                     (text_x + text_size[0] + 5, text_y + 5),
                     (255, 255, 255), -1)

        # Draw text
        cv2.putText(output, tag_id, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                   (255, 0, 0), thickness)

        # Draw corner labels (optional, for debugging)
        corner_labels = ['LB', 'RB', 'RT', 'LT']
        for i, label in enumerate(corner_labels):
            pt = tuple(corners[i])
            cv2.circle(output, pt, 3, (255, 0, 255), -1)

    return output


def main():
    if len(sys.argv) < 2:
        print("Usage: python visualize_detections.py <image_path> [tag_family]")
        print("Example: python visualize_detections.py image.jpg tag36h11")
        sys.exit(1)

    image_path = sys.argv[1]
    tag_family = sys.argv[2] if len(sys.argv) > 2 else 'tag36h11'

    # Load image
    print(f"Loading image: {image_path}")
    color_image = cv2.imread(image_path)

    if color_image is None:
        print(f"Error: Could not load image from {image_path}")
        sys.exit(1)

    # Convert to grayscale for detection
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

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
    detections = detector.detect(gray_image)

    print(f"Found {len(detections)} tag(s)")

    # Draw detections
    output_image = draw_detections(color_image, detections)

    # Display result
    cv2.imshow('AprilTag Detections', output_image)
    print("\nPress any key to close the window...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Optionally save result
    output_path = image_path.rsplit('.', 1)[0] + '_detected.jpg'
    cv2.imwrite(output_path, output_image)
    print(f"Saved result to: {output_path}")


if __name__ == '__main__':
    main()
