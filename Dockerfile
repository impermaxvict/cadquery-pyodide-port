FROM pyodide/pyodide:0.19.0

ARG BUILDER_USER="pyusr"

RUN \
	groupadd -r "${BUILDER_USER}" \
	&& \
	useradd \
		--no-log-init \
		-r \
		--create-home \
		-g "${BUILDER_USER}" \
		"${BUILDER_USER}"

RUN chown -R "${BUILDER_USER}":"${BUILDER_USER}" /src/pyodide/

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
RUN PYODIDE_PACKAGES="occt-debug" make


ADD --chown="${BUILDER_USER}" ./packages/pywrap/ packages/pywrap/
RUN PYODIDE_PACKAGES="pywrap" make


ADD --chown="${BUILDER_USER}" ./packages/ocp-bindings/ packages/ocp-bindings/
RUN PYODIDE_PACKAGES="ocp-bindings" make


ADD --chown="${BUILDER_USER}" ./packages/ocp/ packages/ocp/
RUN PYODIDE_PACKAGES="ocp" make


USER root

FROM scratch

COPY --from=0 /src/pyodide/packages/freetype/build/ /
COPY --from=0 /src/pyodide/packages/rapidjson/build/ /
COPY --from=0 /src/pyodide/packages/occt/build/ /
COPY --from=0 /src/pyodide/packages/pybind11/build/ /
COPY --from=0 /src/pyodide/packages/occt-debug/build/ /
COPY --from=0 /src/pyodide/packages/pywrap/build/ /
COPY --from=0 /src/pyodide/packages/ocp-bindings/build/ /
COPY --from=0 /src/pyodide/packages/ocp/build/ /
