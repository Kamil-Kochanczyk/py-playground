# === Stage 1 ===

FROM node:24-slim AS base

# https://github.com/opencontainers/image-spec/blob/main/annotations.md
# adding metadata to the image
LABEL org.opencontainers.image.authors="sid@devopsdirective.com"

# node's path convention
WORKDIR /usr/src/app/

# dependencies should be copied before source code is copied
# COPY supports basic copying of files into the container, from the build context or from a stage in a multi-stage build
# there is also functionally similar ADD
# ADD supports features for fetching files from remote HTTPS and Git URLs, and extracting tar files automatically when adding files from the build context
COPY package.json package-lock.json ./



# === Stage 2 ===

# preload base's files into prod
FROM base AS prod

# set node's env variable to production to reduce logging, etc.
# this variable is available both at build time and at runtime
ENV NODE_ENV=production

# use cache mount to avoid redownloading all dependencies when a dependency changes
# (previously downloaded dependencies will be stored locally)
RUN --mount=type=cache,target=/usr/src/app/.npm \
  npm set cache /usr/src/app/.npm && \
  npm ci --omit=dev

# set the user to be non-root (node's built-in user)
USER node

# copy only the necessary files (you can also use .dockerignore for this)
# by default the copied files are owned by the root
# chown must be used to change the owner (and the group) of those files to the non-root user
# this prevents "Permission Denied" error
# note: 
# - without "COPY --from=<stage>" the files are copied from the host
# - with "COPY --from=<stage>" the files are copied from one of the previous stages
COPY --chown=node:node ./src/ .

# metadata: where the app is expected to be listened on
EXPOSE 3000

# executable
ENTRYPOINT [ "node" ]

# executable's default argument
CMD [ "index.js" ]



# === Stage 3 ===

FROM base AS dev

# this RUN command is different than in Stage 2
# if they were the same, we would put this RUN command in the base
# Heredocs syntax allows for specifying multiple commands to
# be run within a single step, across multiple lines
# without lots of && and \
# however, it doesn't work here on Windows, for some reason (probably some parsing error)
# RUN --mount=type=cache,target=/usr/src/app/.npm <<EOF
# npm set cache /usr/src/app/.npm
# npm install
# EOF
RUN --mount=type=cache,target=/usr/src/app/.npm npm set cache /usr/src/app/.npm && npm install

COPY ./ ./

# ENTRYPOINT + CMD is the recommended pattern
# however, instead of ENTRYPOINT + CMD you can use only CMD
# in such case you must specify the executable
# use CMD only if you want your image to be flexible and not single-purpose-oriented
CMD [ "npm", "run", "dev" ]