# Type Hints Support

apriltag-python includes full type hints support with **automatically generated** `.pyi` stub files that stay in sync with the C extension.

## Features

- ✅ Auto-generated `.pyi` stub files (not manually maintained)
- ✅ `py.typed` marker file (PEP 561 compliant)
- ✅ Support for mypy, Pylance, Pyright and other type checkers
- ✅ IDE autocomplete and type hints
- ✅ Python 3.10+ modern type syntax

## How It Works

The type stubs are **automatically generated during package build**:

1. When you run `pip install .`, the C extension is built
2. After building, `generate_stubs.py` automatically runs
3. Fresh `apriltag.pyi` file is created with current type definitions
4. The stub file is included in the distribution package

This means:
- ✅ Type definitions always match the C extension
- ✅ No manual maintenance required
- ✅ Automatic updates when AprilTag source changes

## For Users

Just install the package normally:

```bash
pip install apriltag-python
```

The type stubs are automatically included and will work with your IDE.

## For Developers

### Modifying Type Definitions

**Do NOT edit `apriltag.pyi` directly** - it's auto-generated and will be overwritten.

Instead, edit the stub template in `generate_stubs.py`:

```python
# In generate_stubs.py

# To add a new tag family:
TagFamily = Literal[
    'tag36h11',
    'tag36h10',
    # ... existing families ...
    'newFamily'  # Add here
]

# To modify function signatures:
def __init__(
    self,
    family: TagFamily,
    new_param: int = 0  # Add new parameters here
) -> None:
```

Then rebuild to regenerate the stub:

```bash
pip install -e .
```

### Manual Stub Generation

To manually regenerate stubs without building:

```bash
python generate_stubs.py
```

### Verifying Stub Generation

After building, check that stubs were generated:

```bash
# Build and install
pip install -e .

# Verify files exist
ls -la apriltag.pyi py.typed

# Test with mypy
mypy examples/type_checking_example.py
```

## Version Control

You can choose whether to commit `apriltag.pyi` to git:

**Option 1: Commit the stub (recommended for end users)**
- Pros: Users get type hints even without building
- Cons: Need to regenerate and commit after C source changes

**Option 2: Don't commit the stub (recommended for active development)**
- Pros: Always fresh, no manual sync needed
- Cons: Users must build to get type hints

To ignore auto-generated stub in git:
```bash
# Edit .gitignore, uncomment this line:
apriltag.pyi
```

## Example Usage

See [examples/type_checking_example.py](examples/type_checking_example.py) for complete examples with type hints.

Basic usage:

```python
import apriltag
import numpy as np

# IDE shows autocomplete for all parameters
detector: apriltag.apriltag = apriltag.apriltag(
    family='tag36h11',  # IDE autocompletes available families
    threads=4
)

# Type-safe detection
image: np.ndarray = np.zeros((480, 640), dtype=np.uint8)
detections: tuple[apriltag.Detection, ...] = detector.detect(image)

# IDE knows the structure of Detection
for det in detections:
    tag_id: int = det['id']
    center: np.ndarray = det['center']
```

## Documentation

- **[STUB_GENERATION.md](STUB_GENERATION.md)** - Detailed stub generation documentation
- **[TYPE_HINTS.md](TYPE_HINTS.md)** - Type hints usage guide
- **[generate_stubs.py](generate_stubs.py)** - Stub generation script

## Troubleshooting

### Stub file not found after installation

```bash
# Check where the package is installed
python -c "import apriltag, os; print(os.path.dirname(apriltag.__file__))"

# List files in that directory
ls -la <path_from_above>

# Should see: apriltag.pyi and py.typed
```

### Type checker not working

1. Reinstall the package: `pip install --force-reinstall apriltag-python`
2. Restart your IDE
3. Check mypy can see the stubs: `mypy --show-traceback your_script.py`

### Stub is outdated

Rebuild the package to regenerate stubs:

```bash
pip install -e . --force-reinstall --no-deps
```

## Contributing

When modifying the C extension:

1. Update `generate_stubs.py` if type signatures change
2. Run `python generate_stubs.py` to regenerate
3. Test with `mypy examples/type_checking_example.py`
4. Commit both the script and (optionally) the generated stub

## References

- [PEP 561 - Distributing Type Information](https://www.python.org/dev/peps/pep-0561/)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [Stub Generation Documentation](STUB_GENERATION.md)
