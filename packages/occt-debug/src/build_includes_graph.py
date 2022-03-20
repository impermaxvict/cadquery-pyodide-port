#!/usr/bin/env python3

import clang.cindex  # type: ignore

import pathlib
import argparse
import json


def find_compile_commands_database(
    build_tree: pathlib.Path,
) -> clang.cindex.CompilationDatabase:
    assert build_tree.is_dir()
    return clang.cindex.CompilationDatabase.fromDirectory(build_tree)


def get_command_for_file(
    compdb: clang.cindex.CompilationDatabase, source_file_path: pathlib.Path
) -> tuple[pathlib.Path, str, list[str]]:
    assert source_file_path.is_file()

    file_commands = list(compdb.getCompileCommands(source_file_path))
    assert len(file_commands) == 1
    file_command = file_commands[0]
    del file_commands
    return (file_command.directory, file_command.filename, list(file_command.arguments))


def make_relative(
    path: pathlib.Path, cmake_source_tree: pathlib.Path, cmake_build_tree: pathlib.Path
) -> pathlib.Path:
    path = path.resolve()
    if path.is_relative_to(cmake_source_tree):
        return pathlib.Path("$SOURCE") / path.relative_to(cmake_source_tree)
    elif path.is_relative_to(cmake_build_tree):
        return pathlib.Path("$BUILD") / path.relative_to(cmake_build_tree)
    return path


def is_external_file(
    path: pathlib.Path, cmake_source_tree: pathlib.Path, cmake_build_tree: pathlib.Path
) -> bool:
    path = path.resolve()
    return not (
        path.is_relative_to(cmake_source_tree) or path.is_relative_to(cmake_build_tree)
    )


def export_to_graphviz(
    adjacency_list: dict[str, set[str]],
    cmake_source_tree: pathlib.Path,
    cmake_build_tree: pathlib.Path,
) -> str:
    graph: list[str] = []
    graph.append("digraph {")
    graph.append('  splines="ortho"')
    graph.append('  node [shape="box"]')
    for node_from in sorted(adjacency_list):
        if is_external_file(
            pathlib.Path(node_from), cmake_source_tree, cmake_build_tree
        ):
            continue
        node_path_from = make_relative(
            pathlib.Path(node_from), cmake_source_tree, cmake_build_tree
        )
        for node_to in adjacency_list[node_from]:
            if is_external_file(
                pathlib.Path(node_to), cmake_source_tree, cmake_build_tree
            ):
                continue
            node_path_to = make_relative(
                pathlib.Path(node_to), cmake_source_tree, cmake_build_tree
            )
            graph.append(
                '  "' + str(node_path_from) + '" -> "' + str(node_path_to) + '"'
            )
    graph.append("}")
    graph.append("")
    return "\n".join(graph)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find all includes of C++ source files in a folder using the compilation commands database"
    )
    parser.add_argument(
        "cmake_source_tree",
        metavar="cmake-source-tree",
        help="The folder which contains the source files",
        type=pathlib.Path,
    )
    parser.add_argument(
        "cmake_build_tree",
        metavar="cmake-build-tree",
        help="The folder which contains the build files",
        type=pathlib.Path,
    )
    parser.add_argument(
        "source_folder",
        metavar="source-folder",
        help="The folder which contains the source files",
        type=pathlib.Path,
    )
    parser.add_argument(
        "--json",
        help="The JSON output file containing the directed graph of includes",
        type=pathlib.Path,
    )
    parser.add_argument(
        "--graphviz",
        help="The Graphviz output file containing the directed graph of includes",
        type=pathlib.Path,
    )
    args = parser.parse_args()

    assert args.cmake_source_tree.is_dir()
    assert args.cmake_build_tree.is_dir()
    assert args.source_folder.is_dir()

    compdb = find_compile_commands_database(args.cmake_build_tree)

    index = clang.cindex.Index.create()

    all_includes: dict[str, set[str]] = {}

    for source_file in args.source_folder.iterdir():
        if source_file.suffix not in [".cxx", ".lxx", ".gxx"]:
            continue

        if str(source_file) in all_includes:
            continue

        directory, filename, arguments = get_command_for_file(compdb, source_file)

        tu = index.parse(
            None,
            arguments,
            options=clang.cindex.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES,
        )
        if not tu:
            raise Exception("Failed to parse translation unit!")

        for incl in tu.get_includes():
            if not str(incl.source) in all_includes:
                all_includes[str(incl.source)] = set()
            if not str(incl.include) in all_includes[str(incl.source)]:
                all_includes[str(incl.source)].add(str(incl.include))

    if args.json:
        all_includes_lists: dict[str, list[str]] = {}
        for key in all_includes:
            all_includes_lists[key] = list(sorted(all_includes[key]))
        with open(args.json, "w") as fp:
            json.dump(all_includes_lists, fp, sort_keys=True)

    if args.graphviz:
        with open(args.graphviz, "w") as fp:
            fp.write(
                export_to_graphviz(
                    all_includes,
                    args.cmake_source_tree.resolve(),
                    args.cmake_build_tree.resolve(),
                )
            )


if __name__ == "__main__":
    main()
