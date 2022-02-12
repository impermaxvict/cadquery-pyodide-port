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
        # lib = lib.relative_to(OCCT_ROOT / "lib")
        if lib.stem[3:] == "TKXMesh":
            continue
        # libs.append(lib.stem[3:])
        libs.append(lib.resolve())
    libs = list(map(str, libs))
    print(libs)
    return libs


RAPIDJSON_PATH = pathlib.Path(
    "/src/pyodide/packages/rapidjson/build/rapidjson-1.1.0/include/"
)
assert RAPIDJSON_PATH.is_dir()

ext_modules = [
    Extension(
        "OCP",
        list(map(str, sorted(pathlib.Path.cwd().glob("*.cpp")))),
        include_dirs=[
            str(OCCT_ROOT / "include"),
            str(OCCT_ROOT / "include" / "opencascade"),
            str(RAPIDJSON_PATH),
            str(pybind11_include_dir),
        ],
        library_dirs=[
            str(OCCT_ROOT / "lib"),
        ],
        # libraries=find_occt_libs(),
        extra_objects=find_occt_libs(),
    ),
]

setup(
    name="ocp",
    version="7.5.3",
    ext_modules=ext_modules,
    zip_safe=False,
    python_requires=">=3.9",
)
