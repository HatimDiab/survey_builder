.PHONY: build
build: docker-compose.yml stop
	docker compose -f docker-compose.yml build

.PHONY: start
start: docker-compose.yml
	docker compose -f docker-compose.yml up -d

.PHONY: stop
stop: docker-compose.yml
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

.PHONY: clean
clean:
	docker compose down --volumes --remove-orphans
	docker builder prune -f

.PHONY: psql
psql: docker-compose.yml
	docker compose -f docker-compose.yml exec db psql -U survey -d survey_builder

.PHONY: dot
dot: er_diagram.dot
	dot -Tpng er_diagram.dot -o er_diagram.png
	dot -Tpdf er_diagram.dot -o er_diagram.pdf
