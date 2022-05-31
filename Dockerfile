# syntax=docker/dockerfile:1.3
FROM pyodide/pyodide:0.20.0

RUN --network=none useradd --system --user-group --create-home pyodide

RUN --network=none chown -R pyodide:pyodide /src/pyodide/packages/

WORKDIR /src/pyodide/packages/

USER pyodide

RUN pip install /src/pyodide/pyodide-build


RUN --network=none cd sharedlib-test \
	&& python -m pyodide_build buildpkg meta.yaml


RUN --network=none cd sharedlib-test-py \
	&& python -m pyodide_build buildpkg meta.yaml


ADD --chown=pyodide ./packages/occt-raw/ occt-raw
RUN cd occt-raw \
	&& python -m pyodide_build buildpkg meta.yaml


ADD --chown=pyodide ./packages/occt/ occt
RUN --network=none cd occt \
	&& python -m pyodide_build buildpkg meta.yaml


USER root

FROM scratch

COPY --from=0 --chown=root /src/pyodide/packages/occt/build/ /build/occt/
