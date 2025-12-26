#!/usr/bin/env python3
"""
Real-time AprilTag detection from webcam.
Press 'q' to quit.
"""

import apriltag
import cv2
import sys


def main():
    tag_family = sys.argv[1] if len(sys.argv) > 1 else 'tag36h11'

    # Create detector
    print(f"Initializing detector with tag family: {tag_family}")
    detector = apriltag.apriltag(
        family=tag_family,
        threads=4,
        maxhamming=1,
        decimate=2.0,
        blur=0.0,
        refine_edges=True,
        debug=False
    )

    # Open webcam
    print("Opening webcam...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam")
        sys.exit(1)

    print("Webcam opened successfully")
    print("Press 'q' to quit")

    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect tags
        detections = detector.detect(gray)

        # Draw detections
        for detection in detections:
            # Draw corners
            corners = detection['lb-rb-rt-lt'].astype(int)
            for i in range(4):
                pt1 = tuple(corners[i])
                pt2 = tuple(corners[(i + 1) % 4])
                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

            # Draw center
            center = tuple(detection['center'].astype(int))
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # Draw ID
            tag_id = str(detection['id'])
            cv2.putText(frame, tag_id,
                       (center[0] - 10, center[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                       (255, 0, 0), 2)

        # Display count
        cv2.putText(frame, f"Tags: {len(detections)}",
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                   0.7, (0, 255, 0), 2)

        # Show frame
        cv2.imshow('AprilTag Detection', frame)

        # Check for 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("Exiting...")


if __name__ == '__main__':
    main()
