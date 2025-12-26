#!/usr/bin/env python3
"""
Test script to verify stub file generation.

This script tests that:
1. generate_stubs.py can run successfully
2. apriltag.pyi is created
3. py.typed marker exists
4. Generated stub has correct content
"""

import os
import sys
import subprocess
from pathlib import Path


def test_stub_generation():
    """Test that stub generation works correctly."""
    print("=" * 60)
    print("Testing Stub Generation")
    print("=" * 60)

    project_root = Path(__file__).parent
    stub_file = project_root / 'apriltag.pyi'
    py_typed_file = project_root / 'py.typed'
    gen_script = project_root / 'generate_stubs.py'

    # Clean up old files
    print("\n1. Cleaning up old stub files...")
    if stub_file.exists():
        stub_file.unlink()
        print("   Removed existing apriltag.pyi")

    # Run generation script
    print("\n2. Running stub generation script...")
    try:
        result = subprocess.run(
            [sys.executable, str(gen_script)],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            print(f"   ✗ Script failed with code {result.returncode}")
            print(f"   stdout: {result.stdout}")
            print(f"   stderr: {result.stderr}")
            return False

        print("   ✓ Script ran successfully")

    except subprocess.TimeoutExpired:
        print("   ✗ Script timed out")
        return False
    except Exception as e:
        print(f"   ✗ Error running script: {e}")
        return False

    # Check stub file exists
    print("\n3. Checking generated files...")
    if not stub_file.exists():
        print(f"   ✗ Stub file not found: {stub_file}")
        return False
    print(f"   ✓ Stub file created: {stub_file}")

    # Check py.typed exists
    if not py_typed_file.exists():
        print(f"   ✗ py.typed not found: {py_typed_file}")
        return False
    print(f"   ✓ py.typed marker exists")

    # Validate stub content
    print("\n4. Validating stub content...")
    with open(stub_file, 'r', encoding='utf-8') as f:
        content = f.read()

    required_elements = [
        'class apriltag:',
        'def __init__',
        'def detect',
        'class Detection(TypedDict):',
        'TagFamily = Literal[',
        'import numpy',
        '__all__',
    ]

    missing = []
    for element in required_elements:
        if element not in content:
            missing.append(element)

    if missing:
        print("   ✗ Missing required elements:")
        for elem in missing:
            print(f"     - {elem}")
        return False

    print("   ✓ All required elements present")

    # Check file size
    size = len(content)
    print(f"\n5. Stub file statistics:")
    print(f"   Size: {size} bytes")
    print(f"   Lines: {len(content.splitlines())}")

    if size < 1000:
        print("   ⚠ Warning: Stub file seems too small")

    # Verify stub syntax
    print("\n6. Checking Python syntax...")
    try:
        compile(content, str(stub_file), 'exec')
        print("   ✓ Stub has valid Python syntax")
    except SyntaxError as e:
        print(f"   ✗ Syntax error in stub: {e}")
        return False

    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)

    return True


def test_import_after_generation():
    """Test that we can check types after generation."""
    print("\n\nTesting type checking...")

    # Create a test file
    test_code = '''
import apriltag
import numpy as np

detector: apriltag.apriltag = apriltag.apriltag('tag36h11')
image: np.ndarray = np.zeros((480, 640), dtype=np.uint8)
detections: tuple[apriltag.Detection, ...] = detector.detect(image)
'''

    test_file = Path(__file__).parent / 'test_types_temp.py'

    try:
        with open(test_file, 'w') as f:
            f.write(test_code)

        # Try to check with mypy if available
        try:
            result = subprocess.run(
                ['mypy', '--no-error-summary', str(test_file)],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                print("✓ Type checking passed with mypy")
            else:
                print("⚠ mypy found issues (this may be expected if extension isn't built):")
                print(result.stdout)

        except FileNotFoundError:
            print("ℹ mypy not installed, skipping type check test")

    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()


def main():
    """Main test function."""
    success = test_stub_generation()

    if success:
        test_import_after_generation()
        return 0
    else:
        print("\n✗ Stub generation tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
