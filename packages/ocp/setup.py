from setuptools import setup

from pybind11.setup_helpers import Pybind11Extension, build_ext

import pathlib

OCCT_ROOT = pathlib.Path("/src/pyodide/packages/occt/build/occt-V7_5_3p1/install/")


def find_occt_libs():
    libs = []
    for lib in sorted((OCCT_ROOT / "lib").glob("lib*.a")):
        # lib = lib.relative_to(OCCT_ROOT / "lib")
        if lib.stem[3:] == "TKXMesh":
            continue
        # libs.append(lib.stem[3:])
        libs.append(lib.resolve())
    libs = list(map(str, libs))
    print("OCCT libraries:")
    print(libs)
    return libs


RAPIDJSON_PATH = pathlib.Path(
    "/src/pyodide/packages/rapidjson/build/rapidjson-1.1.0/include/"
)

ext_modules = [
    Pybind11Extension(
        "OCP",
        list(map(str, sorted(pathlib.Path.cwd().glob("*.cpp")))),
        include_dirs=[
            "OCP",
            str(OCCT_ROOT / "include" / "opencascade"),
            str(RAPIDJSON_PATH),
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
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
)
