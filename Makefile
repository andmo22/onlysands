APP_SERVICE=onlysands-app-1
DB_SERVICE=onlysands-db-1
WORKDIR=$(shell pwd)
.PHONY: psql

setup:
	docker compose down
	docker compose build
	docker compose up -d

stop:
	docker compose down

clean: stop
	docker compose down --volumes --rmi all

restart: stop setup

logs:
	docker compose logs -f $(APP_SERVICE)
	
exec:
	@if [ "$$OS" = "Windows_NT" ]; then \
		winpty docker exec -it $(APP_SERVICE) bash; \
	else \
		docker exec -it $(APP_SERVICE) /bin/sh; \
	fi

shell: exec

push:
	docker tag onlysands-app:latest andmo22/onlysands-app:latest
	docker push andmo22/onlysands-app:latest
	
deploy-test:
	kubectl delete pod -l 'app in (django)' --namespace onlysands-test
