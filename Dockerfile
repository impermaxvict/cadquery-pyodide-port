# syntax=docker/dockerfile:1.3
FROM pyodide/pyodide:0.19.0

ARG BUILDER_USER="pyusr"

RUN --network=none useradd --system --user-group "${BUILDER_USER}"

RUN --network=none chown -R "${BUILDER_USER}":"${BUILDER_USER}" /src/pyodide/

WORKDIR /src/pyodide/

USER "${BUILDER_USER}"


USER root
RUN apt update && apt install -y libclang-dev
USER "${BUILDER_USER}"


ADD --chown="${BUILDER_USER}" ./packages/freetype/ packages/freetype/
RUN PYODIDE_PACKAGES="freetype" make


ADD --chown="${BUILDER_USER}" ./packages/rapidjson/ packages/rapidjson/
RUN PYODIDE_PACKAGES="rapidjson" make


ADD --chown="${BUILDER_USER}" ./packages/occt/ packages/occt/
RUN PYODIDE_PACKAGES="occt" make


ADD --chown="${BUILDER_USER}" ./packages/pybind11/ packages/pybind11/
RUN PYODIDE_PACKAGES="pybind11" make


ADD --chown="${BUILDER_USER}" ./packages/occt-debug/ packages/occt-debug/
RUN --network=none PYODIDE_PACKAGES="occt-debug" make


ADD --chown="${BUILDER_USER}" ./packages/pywrap/ packages/pywrap/
RUN PYODIDE_PACKAGES="pywrap" make


ADD --chown="${BUILDER_USER}" ./packages/ocp-bindings/ packages/ocp-bindings/
RUN PYODIDE_PACKAGES="ocp-bindings" make


ADD --chown="${BUILDER_USER}" ./packages/ocp/ packages/ocp/
RUN --network=none PYODIDE_PACKAGES="ocp" make


USER root

FROM scratch

COPY --from=0 /src/pyodide/packages/occt-debug/build/ /build/occt-debug/
