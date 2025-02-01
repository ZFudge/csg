.PHONY: help
help:
	@echo "Usage: make [command]"
	@echo "Commands:"
	@echo "  run:                   Run the containers"
	@echo "  stop:                  Stop the containers"
	@echo "  clean:                 Stop and remove the containers"
	@echo "  shell-fe:              Open a shell in the frontend container"
	@echo "  shell-be:              Open a shell in the backend container"
	@echo "  logs:                  Show the logs of the containers"
	@echo "  static:                Build the frontend static files"
	@echo "  help:                  Show this help message"
	@echo "  build:                 Build the containers"
	@echo ""

.PHONY: build
build:
	@docker-compose build

.PHONY: run
run: clean
	@docker-compose up -d

.PHONY: clean
clean: stop
	@docker-compose rm -f

.PHONY: stop
stop:
	@docker-compose down

.PHONY: logs
logs:
	@docker-compose logs --follow


shell-fe:
	@docker-compose exec -it csg-fe-dev sh

.PHONY: install
install:
	@docker-compose exec -it csg-fe-dev sh -c 'pnpm install'

.PHONY: static
static:
	@docker-compose exec -it csg-fe-dev sh -c 'pnpm build'

shell-be:
	@docker-compose exec -it csg-be-dev sh
