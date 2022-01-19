FROM pyodide/pyodide:0.18.0

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

RUN chown -R "${BUILDER_USER}":"${BUILDER_USER}" /src/

USER "${BUILDER_USER}"



USER root
RUN apt update && apt install -y libclang-dev
USER "${BUILDER_USER}"



USER root
ADD ./packages/freetype/ /src/pyodide/packages/freetype/
RUN chown -R "${BUILDER_USER}":"${BUILDER_USER}" \
	/src/pyodide/packages/freetype/
USER "${BUILDER_USER}"

RUN \
	cd /src/pyodide/ \
	&& \
	PYODIDE_PACKAGES="freetype" make



USER root
ADD ./packages/rapidjson/ /src/pyodide/packages/rapidjson/
RUN chown -R "${BUILDER_USER}":"${BUILDER_USER}" \
	/src/pyodide/packages/rapidjson/
USER "${BUILDER_USER}"

RUN \
	cd /src/pyodide/ \
	&& \
	PYODIDE_PACKAGES="rapidjson" make



USER root
ADD ./packages/occt/ /src/pyodide/packages/occt/
RUN chown -R "${BUILDER_USER}":"${BUILDER_USER}" \
	/src/pyodide/packages/occt/
USER "${BUILDER_USER}"

RUN \
	cd /src/pyodide/ \
	&& \
	PYODIDE_PACKAGES="occt" make



USER root
ADD ./packages/ocp/ /src/pyodide/packages/ocp/
RUN chown -R "${BUILDER_USER}":"${BUILDER_USER}" \
	/src/pyodide/packages/ocp/
USER "${BUILDER_USER}"

RUN \
	cd /src/pyodide/ \
	&& \
	PYODIDE_PACKAGES="ocp" make



USER root

FROM scratch

COPY --from=0 /src/pyodide/packages/freetype/build/ /
COPY --from=0 /src/pyodide/packages/rapidjson/build/ /
COPY --from=0 /src/pyodide/packages/occt/build/ /
COPY --from=0 /src/pyodide/packages/ocp/build/ /
