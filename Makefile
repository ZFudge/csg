FE_CONTAINER := csg-fe-dev
BE_CONTAINER := csg-be
STATIC_VOLUME := static-vol

.PHONY: help
help:
	@echo "Usage: make [command]"
	@echo "Commands:"
	@echo "  help:                  Show this help message"
	@echo "  build:                 Build the containers"
	@echo "  run:                   Run the containers"
	@echo "  clean:                 Stop and remove the containers"
	@echo "  logs:                  Show the logs of the containers"
	@echo "  shell-fe:              Open a shell in the frontend container"
	@echo "  static:                Build the frontend static files"
	@echo "  install:               Install the frontend dependencies"
	@echo "  storybook:             Start the storybook server"
	@echo "  storybook-build:       Production build of storybook, for performance testing"
	@echo "  shell-be:              Open a shell in the backend container"

.PHONY: build
build:
	@docker compose build

.PHONY: run
run: clean
	@docker compose up -d

.PHONY: clean
clean:
	@docker compose down --remove-orphans
	@docker rm -f $(FE_CONTAINER) $(BE_CONTAINER) || true

.PHONY: logs
logs:
	@docker compose logs --follow

shell-fe:
	@docker compose exec -it $(FE_CONTAINER) bash

.PHONY: install
install:
	@docker run --rm -v $(shell pwd)/frontend/node_modules:/frontend/node_modules csg-fe:latest pnpm install

.PHONY: static
static:
	@docker run --rm -v $(shell pwd)/frontend/node_modules:/frontend/node_modules -v static-vol:/frontend/build csg-fe:latest pnpm build

.PHONY: storybook
storybook:
	@docker compose exec -it $(FE_CONTAINER) sh -c 'pnpm storybook'

.PHONY: storybook-build
storybook-build:
	@docker compose exec -it $(FE_CONTAINER) sh -c 'pnpm build-storybook'

shell-be:
	@docker compose exec -it $(BE_CONTAINER) sh

shell-nginx:
	@docker compose exec -it csg-nginx sh

all: build install static run

nuke:
	@docker compose down --remove-orphans
	@docker rm -f $(FE_CONTAINER) $(BE_CONTAINER) $(NGINX_CONTAINER) || true
	@docker rmi csg-fe:latest csg-be:latest || true
