# syntax=docker/dockerfile:1.3
FROM pyodide/pyodide:0.19.0

RUN --network=none useradd --system --user-group pyodide

RUN --network=none chown -R pyodide:pyodide /src/pyodide/

WORKDIR /src/pyodide/

USER pyodide


USER root
RUN apt update && apt install -y libclang-dev
USER pyodide


ADD --chown=pyodide ./packages/freetype/ packages/freetype/
RUN PYODIDE_PACKAGES="freetype" make


ADD --chown=pyodide ./packages/rapidjson/ packages/rapidjson/
RUN PYODIDE_PACKAGES="rapidjson" make


ADD --chown=pyodide ./packages/occt/ packages/occt/
RUN PYODIDE_PACKAGES="occt" make


ADD --chown=pyodide ./packages/pybind11/ packages/pybind11/
RUN PYODIDE_PACKAGES="pybind11" make


ADD --chown=pyodide ./packages/occt-debug/ packages/occt-debug/
RUN --network=none PYODIDE_PACKAGES="occt-debug" make


ADD --chown=pyodide ./packages/pywrap/ packages/pywrap/
RUN PYODIDE_PACKAGES="pywrap" make


ADD --chown=pyodide ./packages/ocp-bindings/ packages/ocp-bindings/
RUN PYODIDE_PACKAGES="ocp-bindings" make


ADD --chown=pyodide ./packages/ocp/ packages/ocp/
RUN --network=none PYODIDE_PACKAGES="ocp" make


USER root

FROM scratch

COPY --from=0 /src/pyodide/packages/occt-debug/build/ /build/occt-debug/
