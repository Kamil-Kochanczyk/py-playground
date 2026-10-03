# syntax=docker/dockerfile:1
# escape=\

# Optional directives: pull the latest stable Dockerfile syntax before the build and set esc char

# ARG enables setting variables at build time that do not persist in the final image (but can be seen in the image metadata)
# those variables can be overriden at build-time using "docker build --build-arg BASE_IMG_TAG=16.1-alpine ...", for example
# build time is not the same as runtime
# build time is when the image is being built, runtime is when the container is being run
ARG BASE_IMG_TAG=15.1-alpine

FROM postgres:${BASE_IMG_TAG}

# providing sensitive credentials required at build time while keeping them out of the final image
# this is a built-time secret, a feature provided by BuildKit
# its source needs to be specified in the command line when building the image
RUN --mount=type=secret,id=secret.txt,dst=/container-secret.txt \
  echo "Loaded secret during build; use it for built-time configuration only" && \
  echo "Secret content:" && \
  cat /container-secret.txt

# these variables are available both at build time and at runtime and can be seen in the image metadata
# they can be overriden for example using "docker run -e POSTGRES_USER=..."
# here we give them default values
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=postgres
ENV POSTGRES_PASSWORD_FILE=/run/secrets/postgres-password

EXPOSE 5432

VOLUME [ "/var/lib/postgresql/data" ]

CMD [ "postgres" ]
