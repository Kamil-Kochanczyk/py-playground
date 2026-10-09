# ============================================================
# Version 1 (composed db, api (backend) and client (frontend))
# ============================================================

.PHONY: build-webapp-prod
build-webapp-prod:
	@echo Building webapp-prod containers
	docker compose -f docker-compose-prod.yml build

.PHONY: up-webapp-prod
up-webapp-prod:
	@echo Starting webapp-prod containers
	docker compose -f docker-compose-prod.yml up -d

.PHONY: down-webapp-prod
down-webapp-prod:
	@echo Stopping and removing webapp-prod containers
	docker compose -f docker-compose-prod.yml down

.PHONY: build-webapp-dev
build-webapp-dev:
	@echo Building webapp-dev containers
	docker compose -f docker-compose-dev.yml build

.PHONY: up-webapp-dev
up-webapp-dev:
	@echo Starting webapp-dev containers
	docker compose -f docker-compose-dev.yml up -d

.PHONY: down-webapp-dev
down-webapp-dev:
	@echo Stopping and removing webapp-dev containers
	docker compose -f docker-compose-dev.yml down

.PHONY: build-webapp-debug
build-webapp-debug:
	@echo Building webapp-debug containers
	docker compose -f docker-compose-dev.yml -f docker-compose-debug.yml build

.PHONY: up-webapp-debug
up-webapp-debug:
	@echo Starting webapp-debug containers
	docker compose -f docker-compose-dev.yml -f docker-compose-debug.yml up -d

.PHONY: down-webapp-debug
down-webapp-debug:
	@echo Stopping and removing webapp-debug containers
	docker compose -f docker-compose-dev.yml -f docker-compose-debug.yml down

.PHONY: build-webapp-test
build-webapp-test:
	@echo Building webapp-test containers
	docker compose -f docker-compose-dev.yml -f docker-compose-test.yml build

.PHONY: up-webapp-test
up-webapp-test:
	@echo Starting webapp-test containers
	docker compose -f docker-compose-dev.yml -f docker-compose-test.yml run --rm webapp-backend

.PHONY: down-webapp-test
down-webapp-test:
	@echo Stopping and removing webapp-test containers
	docker compose -f docker-compose-dev.yml -f docker-compose-test.yml down





# =========================================================================
# Version 2 (deprecated) (dockerized db, dockerized api, dockerized client)
# =========================================================================

# This version uses the dockerized db, api and client
# Contrary to the version below, in this version db, api and client are dockerized using their own Dockerfiles
# To run the following commands, first you have to build the three images: one for db, one for api and one for client
# You can build both production images and development images using the provided Dockerfiles
# A still better approach would be to compose the three separate images in one file

# Note that using an env file with a URL containing password is not the safest option for an API to connect to a DB

# If using this version make sure the published frontend's port is correct
# This is because frontend operates on a different port in production mode (8080) and in development mode (5173)
# Also make sure that in vite.config.js the target url uses the network alias specified here (e.g. target: 'http://api-node:3000')

# NETWORK:=webapp-net
# POSTGRES_PSWD_FILE:=/run/secrets/postgres-password

# .PHONY: run-postgres-dock
# run-postgres-dock:
# 	@echo Starting postgres container
# 	-docker run -d --rm \
# 		--name "webapp-postgres-dock" \
# 		--network $(NETWORK) \
# 		--network-alias postgres \
# 		-e POSTGRES_USER=postgres \
# 		-e POSTGRES_DB=postgres \
# 		-e POSTGRES_PASSWORD_FILE=$(POSTGRES_PSWD_FILE) \
# 		-p 5432:5432 \
# 		-v "$(subst \,/,$(CURDIR))/webapp-db/secret.txt:$(POSTGRES_PSWD_FILE):ro" \
# 		webapp-db:1.0

# .PHONY: run-api-node-dock
# run-api-node-dock:
# 	@echo Starting node api
# 	-docker run -d --rm \
# 		--name "webapp-api-node-dock" \
# 		--network ${NETWORK} \
# 		--network-alias api-node \
# 		--env-file "$(CURDIR)/webapp-db/.env" \
# 		-p 3000:3000 \
# 		webapp-backend:1.0

# .PHONY: run-client-react-dock
# run-client-react-dock:
# 	@echo Starting react client
# 	docker run -d --rm \
# 		--name "webapp-client-react-dock" \
# 		--network $(NETWORK) \
# 		--network-alias client-react \
# 		-p 8080:8080 \
# 		webapp-frontend:1.0

# .PHONY: stop-webapp-dock
# stop-webapp-dock:
# 	@echo Stopping webapp containers
# 	docker stop webapp-postgres-dock webapp-api-node-dock webapp-client-react-dock

# .PHONY: rm-webapp-dock
# rm-webapp-dock:
# 	@echo Removing webapp containers
# 	docker rm webapp-postgres-dock webapp-api-node-dock webapp-client-react-dock





# ===============================================================================
# Version 3 (deprecated) (undockerized db, undockerized api, undockerized client)
# ===============================================================================

# This version runs the database, the backend (api) and the frontend (client) using dockerized postgres and node
# Here, the backend and the frontend are treated as not fully dockerized (they're only using the dockerized node)
# In other words: the backend and the frontend run locally and are not built as images themselves
# The backend and the frontend can of course be dockerized and this is actually the recommended approach

# If using this approach, set url in .env file to the following:
# DATABASE_URL=postgres://postgres:<example_password_here>@host.docker.internal:5432/postgres
# If using this approach, set target in vite.config.js file to the following:
# target: 'http://host.docker.internal:3000'

# Note that normally you shouldn't put a URL with password inside a file that is committed to a version control system

# POSTGRES_PSWD_FILE:=/run/secrets/postgres-password

# .PHONY: run-postgres
# run-postgres:
# 	@echo Starting postgres container
# 	-docker run -d --rm \
# 		--name "webapp-postgres" \
# 		--network webapp-api-db \
# 		-e POSTGRES_USER=postgres \
# 		-e POSTGRES_DB=postgres \
# 		-e POSTGRES_PASSWORD_FILE=$(POSTGRES_PSWD_FILE) \
# 		-p 5432:5432 \
# 		-v pgdata:/var/lib/postgresql/data \
# 		-v "$(subst \,/,$(CURDIR))/webapp-db/secret.txt:$(POSTGRES_PSWD_FILE):ro" \
# 		postgres:15.1-alpine

# .PHONY: run-api-node
# run-api-node:
# 	@echo Starting node api
# 	-docker run -d --rm --entrypoint sh \
# 		--add-host=host.docker.internal:host-gateway \
# 		--name "webapp-api-node" \
# 		--network webapp-api-db \
# 		--network webapp-client-api \
# 		--env-file "$(CURDIR)/webapp-db/.env" \
# 		-p 3000:3000 \
# 		-v "$(subst \,/,$(CURDIR))/api-node:/app-node" \
# 		-w /app-node \
# 		node:24-slim -lc "npm run dev"

# .PHONY: run-client-react
# run-client-react:
# 	@echo Starting react client
# 	docker run -d --rm --entrypoint sh \
# 		--add-host=host.docker.internal:host-gateway \
# 		--name "webapp-client-react" \
# 		--network webapp-client-api \
# 		-p 5173:5173 \
# 		-v "$(subst \,/,$(CURDIR))/client-react:/app-react" \
# 		-w /app-react \
# 		node:24-slim -lc "npm run dev"

# .PHONY: stop-webapp
# stop-webapp:
# 	@echo Stopping webapp containers
# 	docker stop webapp-postgres webapp-api-node webapp-client-react

# .PHONY: rm-webapp
# rm-webapp:
# 	@echo Removing webapp containers
# 	docker rm webapp-postgres webapp-api-node webapp-client-react





# ===============================================================================
# Notes
# ===============================================================================

# By default, a Docker container runs inside an isolated network. 
# If your application running inside the container needs to talk to something running directly on your host machine 
# (like a local PostgreSQL database or another app), 
# the container won't know what localhost means — to the container, localhost refers to itself.
#
# --add-host: Tells Docker to add an entry to the container's internal /etc/hosts DNS file (mapping a domain name to an IP address).
# host.docker.internal: The domain name your Node.js code can use to address your machine (e.g., connecting to host.docker.internal:5432).
# host-gateway: A special Docker keyword that dynamically resolves to the internal IP address of your host machine's network gateway.

# $(subst \,/,$(CURDIR))
# This is a GNU Make function, not a Docker flag. It ensures cross-platform compatibility (specifically for Windows users).
# $(CURDIR): A built-in Make variable that holds the absolute path to the directory where the Makefile lives.
# subst search,replace,text: Replaces every instance of search with replace.
# $(subst \,/, ...): Converts Windows-style backslashes (C:\project) into POSIX-style forward slashes (C:/project).
#
# Docker on Linux or WSL can fail if volume mount paths contain backslashes.

# --entrypoint sh overrides the container's default startup command and replaces it with the Unix Shell (sh)
# -l (login shell): Forces sh to act as a login shell, loading shell profile scripts (like /etc/profile or ~/.profile) so all environment variables and PATH configurations are properly loaded.
# -c (command): Tells sh to read and execute the string that follows it as a command, then exit.
# Together, -lc "npm run dev" tells Docker: "Start a login shell, run npm run dev inside it, and keep that process alive."
