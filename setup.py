import os
import sys
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import numpy as np


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the following extensions: " +
                ", ".join(e.name for e in self.extensions))

        for ext in self.extensions:
            self.build_extension(ext)

        # Generate type stubs after building
        self.generate_stubs()

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        # Create build directory
        build_temp = os.path.join(self.build_temp, 'apriltag')
        os.makedirs(build_temp, exist_ok=True)

        cmake_args = [
            f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}',
            f'-DPYTHON_EXECUTABLE={sys.executable}',
            '-DBUILD_PYTHON_WRAPPER=ON',
            '-DBUILD_EXAMPLES=OFF',
            '-DBUILD_SHARED_LIBS=ON',
        ]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        cmake_args += [f'-DCMAKE_BUILD_TYPE={cfg}']

        # Parallel build
        build_args += ['--', '-j4']

        env = os.environ.copy()
        env['CXXFLAGS'] = f'{env.get("CXXFLAGS", "")} -DVERSION_INFO=\\"{self.distribution.get_version()}\\"'

        # Run CMake
        subprocess.check_call(['cmake', ext.sourcedir + '/apritag'] + cmake_args,
                            cwd=build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args,
                            cwd=build_temp)

    def generate_stubs(self):
        """Generate type stub files after building extension."""
        print("Generating type stubs...")

        # Run the stub generation script
        stub_script = os.path.join(os.path.dirname(__file__), 'generate_stubs.py')

        if os.path.exists(stub_script):
            try:
                subprocess.check_call([sys.executable, stub_script])
                print("Type stubs generated successfully")
            except subprocess.CalledProcessError as e:
                print(f"Warning: Failed to generate type stubs: {e}")
                print("Continuing with build...")
        else:
            print(f"Warning: Stub generation script not found at {stub_script}")
            print("Skipping stub generation...")


# Read long description from README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read version from apriltag CMakeLists.txt
version = '3.4.5'

setup(
    name='apriltag-python',
    version=version,
    author='AprilRobotics Team, chibai',
    author_email='',
    description='Python wrapper for AprilTag visual fiducial detector',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chibai/apriltag-python',
    license='BSD-2-Clause',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: C',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
    ],
    keywords='apriltag, fiducial, marker, detection, computer vision, robotics',
    python_requires='>=3.10',
    install_requires=[
        'numpy>=1.17.0',
    ],
    ext_modules=[CMakeExtension('apriltag')],
    cmdclass={'build_ext': CMakeBuild},
    package_data={
        '': ['*.pyi', 'py.typed'],  # Include type stub files and typing marker
    },
    data_files=[('', ['apriltag.pyi', 'py.typed'])],
    zip_safe=False,
    project_urls={
        'Bug Reports': 'https://github.com/chibai/apriltag-python/issues',
        'Source': 'https://github.com/chibai/apriltag-python',
        'AprilTag C Library': 'https://github.com/AprilRobotics/apriltag',
    },
)
