COMPOSE ?= docker-compose -f docker-compose.yml

run:
	$(COMPOSE) up --build --force-recreate -d

rm:
	$(COMPOSE) rm -sfv

lint:
	@flake8
