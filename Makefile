COMPOSE ?= docker-compose -f docker-compose.yml

run:
	$(COMPOSE) up --build --force-recreate -d

rm:
	$(COMPOSE) rm -sfv

log:
	$(COMPOSE) logs -f muzlag 

create-log-file:
	@sudo touch /var/log/muzlag.log
	@sudo chmod a+rwx muzlag.log
	@echo file muzlag.log is created

lint:
	@flake8
