# syntax=docker/dockerfile:1.3
FROM pyodide/pyodide:0.20.0

RUN --network=none useradd --system --user-group --create-home pyodide

RUN --network=none chown -R pyodide:pyodide /src/pyodide/packages/

WORKDIR /src/pyodide/packages/

USER pyodide

RUN pip install ../pyodide-build


RUN --network=none cd sharedlib-test \
	&& python -m pyodide_build buildpkg meta.yaml


RUN --network=none cd sharedlib-test-py \
	&& python -m pyodide_build buildpkg meta.yaml


USER root
RUN apt update && apt install -y libclang-dev && rm -rf /var/lib/apt/lists/*
USER pyodide


ADD --chown=pyodide ./packages/freetype/ freetype
RUN cd freetype \
	&& python -m pyodide_build buildpkg meta.yaml


ADD --chown=pyodide ./packages/rapidjson/ rapidjson
RUN cd rapidjson \
	&& python -m pyodide_build buildpkg meta.yaml


ADD --chown=pyodide ./packages/occt-raw/ occt-raw
RUN cd occt-raw \
	&& python -m pyodide_build buildpkg meta.yaml


ADD --chown=pyodide ./packages/occt/ occt
RUN --network=none cd occt \
	&& python -m pyodide_build buildpkg meta.yaml


ADD --chown=pyodide ./packages/pybind11/ pybind11
RUN cd pybind11 \
	&& python -m pyodide_build buildpkg meta.yaml


ADD --chown=pyodide ./packages/occt-debug/ occt-debug
RUN --network=none cd occt-debug \
	&& python -m pyodide_build buildpkg meta.yaml


ADD --chown=pyodide ./packages/pywrap/ pywrap
RUN cd pywrap \
	&& python -m pyodide_build buildpkg meta.yaml


ADD --chown=pyodide ./packages/ocp-bindings/ ocp-bindings
RUN cd ocp-bindings \
	&& python -m pyodide_build buildpkg meta.yaml


ADD --chown=pyodide ./packages/ocp/ ocp
RUN --network=none cd ocp \
	&& python -m pyodide_build buildpkg meta.yaml


USER root

FROM scratch

COPY --from=0 --chown=root /src/pyodide/packages/occt-debug/build/ /build/occt-debug/
