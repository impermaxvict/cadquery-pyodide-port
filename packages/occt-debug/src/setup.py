from setuptools import setup, Extension

import pathlib

OCCT_ROOT = pathlib.Path("/src/pyodide/packages/occt/build/occt-7.5.3/install/")
assert OCCT_ROOT.is_dir()

pybind11_include_dir = pathlib.Path(
    "/src/pyodide/packages/pybind11/build/pybind11-2.9.1/include/"
)
assert pybind11_include_dir.is_dir()


def find_occt_libs() -> list[str]:
    libraries: list[str] = []

    # https://dev.opencascade.org/doc/refman/html/index.html

    # Module FoundationClasses
    libraries.extend(["TKernel", "TKMath"])

    # Module ModelingData
    libraries.extend(["TKG2d", "TKG3d", "TKGeomBase", "TKBRep"])

    # The order of objects matters!
    libs: list[pathlib.Path] = []
    for lib in reversed(libraries):
        libs.append((OCCT_ROOT / "lib" / ("lib" + lib + ".a")).resolve())
    return list(map(str, libs))


ext_modules = [
    Extension(
        "OCCTDebug",
        list(map(str, sorted(pathlib.Path.cwd().glob("*.cpp")))),
        include_dirs=[
            str(OCCT_ROOT / "include"),
            str(OCCT_ROOT / "include" / "opencascade"),
            str(pybind11_include_dir),
        ],
        library_dirs=[
            str(OCCT_ROOT / "lib"),
        ],
        extra_objects=find_occt_libs(),
    ),
]

setup(
    name="occt-debug",
    version="0.0.0",
    ext_modules=ext_modules,
    zip_safe=False,
    python_requires=">=3.9",
)
