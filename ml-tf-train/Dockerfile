FROM simcore/services/comp/common:0.0.0 AS service-base

LABEL maintainer="Elisabetta Iavarone <iavarone@itis.swiss>"


COPY --chown=${SC_USER_NAME}:${SC_USER_ID} src src
WORKDIR /home/${SC_USER_NAME}


# copy simcore service cli
COPY --chown=${SC_USER_NAME}:${SC_USER_NAME} service.cli/ service.cli/

ENTRYPOINT [ "/bin/sh", "/app/entrypoint.sh", "/bin/sh", "-c" ]
#CMD ["run"] 