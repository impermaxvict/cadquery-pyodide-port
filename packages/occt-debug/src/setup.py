from setuptools import setup, Extension

import pathlib

OCCT_ROOT = pathlib.Path("/src/pyodide/packages/occt/build/occt-7.5.3/install/")
assert OCCT_ROOT.is_dir()

pybind11_include_dir = pathlib.Path(
    "/src/pyodide/packages/pybind11/build/pybind11-2.9.1/include/"
)
assert pybind11_include_dir.is_dir()


def find_occt_libs():
    libs = []
    for lib in sorted((OCCT_ROOT / "lib").glob("lib*.a")):
        # if lib.stem[3:] != "TKernel":
        #    continue
        # https://dev.opencascade.org/doc/refman/html/index.html
        if lib.stem[3:] in ["TKernel", "TKMath"]:
            # Module FoundationClasses
            libs.append(lib.resolve())
        elif lib.stem[3:] in ["TKG2d", "TKG3d", "TKGeomBase", "TKBRep"]:
            # Module ModelingData
            libs.append(lib.resolve())
    libs = list(map(str, libs))
    return libs


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
        # libraries=find_occt_libs(),
        extra_objects=find_occt_libs(),
        extra_compile_args=["-O0"],
    ),
]

setup(
    name="occt-debug",
    version="0.0.0",
    ext_modules=ext_modules,
    zip_safe=False,
    python_requires=">=3.9",
)
