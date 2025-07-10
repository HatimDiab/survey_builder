.PHONY: build
build: docker-compose.yml
	docker compose -f docker-compose.yml build

.PHONY: up
up: docker-compose.yml
	docker compose -f docker-compose.yml up -d

.PHONY: down
down: docker-compose.yml
	docker compose -f docker-compose.yml down --remove-orphans

.PHONY: restart
restart: docker-compose.yml
	docker compose -f docker-compose.yml restart

.PHONY: logs
logs: docker-compose.yml
	docker compose -f docker-compose.yml logs -f

.PHONY: open
open: docker-compose.yml
	open http://localhost:3000