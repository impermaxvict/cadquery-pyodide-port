import pathlib
import os
import toml

OCCT_INCLUDE_DIR = (
    pathlib.Path(os.environ.get("PYODIDE_ROOT", "/src/pyodide"))
    / "packages/occt/build/occt-V7_5_3p1/install/include/opencascade/"
)
assert OCCT_INCLUDE_DIR.is_dir()


def find_available_modules():
    include_dir = OCCT_INCLUDE_DIR
    modules = set()
    for include_file in include_dir.iterdir():
        module_name = include_file.relative_to(include_dir)
        module_name = module_name.name.split(".")[0].split("_")[0]
        modules.add(module_name)
    return list(sorted(modules))


config_file = pathlib.Path("ocp.toml")

config = toml.load(config_file)

modules = set(find_available_modules())
modules = modules.intersection(config["modules"])
config["modules"] = list(sorted(modules))

print(config["Linux"])
config["Linux"]["symbols"] = "symbols_mangled_emscripten.dat"
del config["Linux"]["modules"]
config["Linux"]["parsing_header"] = "#define __EMSCRIPTEN__"
print(config["Linux"])

config["Modules"]["RWGltf"]["exclude_classes"] = ["RWGltf_GltfOStreamWriter"]

if os.environ.get("PYODIDE_ROOT"):
    with open(config_file, "w") as fp:
        toml.dump(config, fp)
else:
    print(toml.dumps(config))
