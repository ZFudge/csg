FE_CONTAINER := csg-fe-dev
BE_CONTAINER := csg-backend

.PHONY: help
help:
	@echo "Usage: make [command]"
	@echo "Commands:"
	@echo "  help:                  Show this help message"
	@echo "  build:                 Build the containers"
	@echo "  run:                   Run the containers"
	@echo "  clean:                 Stop and remove the containers"
	@echo "  logs:                  Show the logs of the containers"
	@echo "  build-be:              Build the backend container"
	@echo "  run-be:                Run the backend container"
	@echo "  shell-fe:              Open a shell in the frontend container"
	@echo "  install:               Install node modules"
	@echo "  static:                Build the frontend static files"
	@echo "  storybook:             Run the storybook server"
	@echo "  storybook-build:       Build the storybook"
	@echo "  shell-be:              Open a shell in the backend container"

.PHONY: build
build:
	@docker-compose build

.PHONY: run
run: clean
	@docker-compose up -d --remove-orphans

.PHONY: clean
clean:
	@docker-compose down --remove-orphans
	@docker rm -f $(FE_CONTAINER) $(BE_CONTAINER) || true

.PHONY: logs
logs:
	@docker-compose logs --follow

.PHONY: build-be
build-be:
	@docker build -t $(BE_CONTAINER) -f backend/Dockerfile backend

.PHONY: run-be
run-be:
	@docker run -p 5075:5075 $(BE_CONTAINER)

# Frontend
shell-fe:
	@docker-compose exec -it $(FE_CONTAINER) bash

.PHONY: install
install:
	@docker-compose exec -it $(FE_CONTAINER) sh -c 'pnpm install'

.PHONY: static
static:
	@docker-compose exec -it $(FE_CONTAINER) sh -c 'pnpm build'

.PHONY: storybook
storybook:
	@docker-compose exec -it $(FE_CONTAINER) sh -c 'pnpm storybook'

.PHONY: storybook-build
storybook-build:
	@docker-compose exec -it $(FE_CONTAINER) sh -c 'pnpm build-storybook'

# Backend
shell-be:
	@docker-compose exec -it $(BE_CONTAINER) sh
