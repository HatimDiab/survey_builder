.PHONY: build
build: docker-compose.yml
	docker compose -f docker-compose.yml build
