########################## LIBRARY IMPORT #############################################
from io import StringIO
import sys
import pathlib

try:
    from skbuild import setup
    from skbuild.exceptions import SKBuildError
except ImportError:
    print(
        "Please update pip, you need pip 10 or greater,\n"
        " or you need to install the PEP 518 requirements in pyproject.toml yourself",
        file=sys.stderr,
    )
    raise


########################## VERSION ####################################################
_ROOT = pathlib.Path(__file__).parent
with open(str(_ROOT / "src" / "inversion_test_problems" / "_version.py")) as f:
    for line in f:
        if line.startswith("__version__="):
            _, _, version = line.partition("=")
            VERSION = version.strip(" \n'\"")
            break
    else:
        raise RuntimeError("unable to read the version from src/inversion_test_problems/_version.py")


########################## LONG DESCRIPTION ###########################################
from pathlib import Path
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()
CONTENT_TYPE = "text/markdown"


########################## OTHER METADATA #############################################
PACKAGE_NAME = "inversion_test_problems"
AUTHOR = f"InLab, {PACKAGE_NAME} development team"
DESCRIPTION = "An inversion test suite that collects examples from many disciplines within geoscience and elsewhere."
KEYWORDS = ["inversion", "inference", "python package", "geoscience", "geophysics"]
CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Education",
    "Intended Audience :: Science/Research",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: C",
    "Programming Language :: Fortran",
    "Topic :: Scientific/Engineering :: Physics",
    # "License :: OSI Approved :: BSD License",
]
PACKAGE_DIR = {"": "src"}
PACKAGES = [PACKAGE_NAME]
CMAKE_INSTALL_DIR = f"src/{PACKAGE_NAME}"
CMAKE_ARGS = ['-DSKBUILD=ON']
PYTHON_REQUIRES = ">=3.6"
INSTALL_REQUIRES = [
    "numpy>=1.18",
    "scipy>=1.0.0",
]
EXTRAS_REQUIRE = {
    "doc": [
        "sphinx", 
        "sphinx-book-theme", 
        "sphinx-panels", 
        "sphinx-togglebutton",
        "sphinx-autobuild",
        "pypandoc",
        "myst-nb",
        "sphinxcontrib-mermaid",
        "sphinx-copybutton",
    ],
}


########################## SETUP ######################################################
class NullIO(StringIO):
    def write(self, txt):
       pass
sys.stdout = NullIO()
sys.tracebacklimit = 0

try:
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        author=AUTHOR,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=CONTENT_TYPE,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        package_dir=PACKAGE_DIR,
        packages=PACKAGES,
        include_package_data=True,
        cmake_install_dir=CMAKE_INSTALL_DIR,
        cmake_args=CMAKE_ARGS,
        python_requires=PYTHON_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
    )
except SystemExit as e:
    skbuild_error : SKBuildError = e.args[0]
    error_message = skbuild_error.args[0]
    error_message += "\n\nHint: search 'error' in current terminal session to find out the details. "
    # error_message += f"Here are some possible reasons that cause failure in building `{PACKAGE_NAME}`:"
    # error_message += "\n\t1. no Fortran compiler found -> install a Fortran compiler and ensure it's included in the path"
    error_message += "\n\n"
    error_message += "If the error is not due to above reasons, "
    error_message += "please feel free to lodge an issue " \
                     f"at https://github.com/inlab-geo/{PACKAGE_NAME}/issues for help\n"
    skbuild_error.args = (error_message,)
    sys.exit(skbuild_error)


# setup(
#     name='inversion-test-problems',
#     version=VERSION,
#     install_requires=[
#         'importlib-metadata; python_version == "3.8"',
#     ],
#     include_package_data=True,
#     #packages=find_packages(exclude=("*.egg_info")),  
#     package_dir={"inversiontestproblems": "contrib"},   # tell distutils packages are under src
# )