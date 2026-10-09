# syntax=docker/dockerfile:1

# pin the base image to a specific digest
# instead you can also use unpinned version
# or configure Dependabot with "package-ecosystem: "docker"" to do automatic updates
FROM python:3.12-slim@sha256:05cda9777409a9c3ffddd94a4c476b79f0769a0b4857f0c7ed9226b6800b0d6f AS builder

# copy uv without installing it into the final image
# uv can be found in GHCR (GitHub Container Registry), in the packages tab
COPY --from=ghcr.io/astral-sh/uv:0.12.8@sha256:d1cbaeadc234fe19c0d93daabcf5e98738cd93c6d1dd4918ef6aa30735feb23a /uv /uvx /usr/local/bin/

# config:
# - compile bytecode (.pyc) upon installation instead of upon the first run (speeds up initial run)
# - perform a full, physical copy of installed packages from uv's global cache into Python's virtual environment (by default, hardlink or reflink mechanism is used)
# - point to the venv directory to setup default, active venv inside the project
# - add the venv directory to the beginning of the PATH env var to use venv's Python and venv's packages by default
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# WORKDIR creates this directory automatically if it doesn't exist
WORKDIR /app

# first dependencies...
COPY pyproject.toml uv.lock README.md LICENSE AUTHORS ./

# make sure "uv sync" doesn't change uv.lock with "uv lock"
# also make sure that it only installs third-party dependencies into venv and doesn't install the project itself
# this is because your project itself can also be a package and uv can also install it into venv
# if you installed the project itself in this step with all third-party dependencies,
# the smallest changes to the source code of your project would invalidate this layer in the cache
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked \
    uv sync --frozen --no-dev --no-install-project

# ...then source code
COPY src/ ./src/

# now we can install only the project itself into the already created venv, without third-party dependencies
RUN --mount=type=cache,target=/root/.cache/uv,sharing=locked \
    uv sync --frozen --no-dev

FROM python:3.12-slim@sha256:05cda9777409a9c3ffddd94a4c476b79f0769a0b4857f0c7ed9226b6800b0d6f AS runtime

# config:
# - point to the venv directory to setup default, active venv inside the project
# - add the venv directory to the beginning of the PATH env var to use venv's Python and venv's packages by default
# - (not used for now) add "/app/src" to "sys.path" (list of paths to search for modules during imports) to provide clean imports ("import module" instead of "import src.module")
# - don't create .pyc (bytecode) files on the import of modules (containers don't persist data, so storing .pyc would be the waste of disk space)
# - force stdout and stderr to write to Docker's logs immediately in real-time, i.e. without buffering (prevents delayed or missing log output during crashes)
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    # PYTHONPATH=/app/src \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# create a non-privileged group (no special permissions, just a blank entry in the list of GIDs)
# create a non-privileged user (no special permissions, no home directory, disable login to prevent the possiblity of running arbitrary commands from the shell)
RUN groupadd -g 10001 appusergroup && \
    useradd -u 10001 -g appusergroup -s /sbin/nologin --no-create-home appuser

# copy the ready venv and the ready Python modules
COPY --from=builder --chown=appuser:appusergroup /app/.venv/ ./.venv/
COPY --from=builder --chown=appuser:appusergroup /app/src/ ./src/

# create the data directory with ownership matching the runtime user
# provide persistence explicitly at runtime with a named volume or bind mount
RUN install -d -o appuser -g appusergroup /app/src/py_playground/expense_tracker/data

# create the volume for persisting data
# note that if you don't mount the volume explicitly
# when running the container with "docker run" command,
# the following VOLUME command creates an anonymous volume, not a named volume
# anonymous volumes get generated names
# so each time you create a container you basically get a new volume
# which makes it harder to reuse the same volume between runs to store persisting data
VOLUME [ "/app/src/py_playground/expense_tracker/data" ]

USER appuser:appusergroup

CMD [ "exp-track-cli" ]

# notes:
# - inode:
# -- index node
# -- data structure which contains metadata and disk locations of files and directories in Unix
# -- it contains metadata such as file type, permissions, size, timestamps, etc.
# -- it contains pointers to locations on disk where the actual data is stored
# -- it doesn't store neither the file's name, nor the actual data (name is stored in directories, data is stored on disk)
# - methods to reference multiple files in OS:
# -- hardlinks, reflinks, symlinks
# - hardlinks:
# -- new name pointing to the same inode (the file has multiple names from the perspective of OS)
# -- file is deleted only if all hardlinks are deleted (deleting one hardlink when others exist doesn't delete the file)
# - reflinks:
# -- reference links, use copy-on-write method
# -- new file with a separate inode but it initially points to the same disk data blocks as the original file/inode (avoids unnecessary duplication)
# -- when reading is requested the shared disk data is safely read from both inodes
# -- when writing is requested only the changed blocks are duplicated to a new location in disk, while the shared blocks remain untouched (data grows on write)
# -- deleting a reflink doesn't affect the other file
# - symlinks:
# -- symbolic links, soft links
# -- new file with a separate inode which contains a textual path reference pointing to the target file
# -- basically a pointer to an existing file in the OS
# -- if the target file is moved, deleted, etc., the symlink becomes broken (dangling link)
# -- deleting the symlink doesn't delete the target file
# - PATH syntax:
# -- PATH is an env var containing a colon-separated list of directory paths where the shell looks for executable commands
# -- ":" (colon) is the standard delimiter used in Unix to separate multiple directory paths
# -- "$PATH" references and expands the current content of the PATH
# -- PATH="/app/.venv/bin:$PATH" prepends "/app/.venv/bin" to the existing contents of the PATH
