APP_ENTRY ?= app:app
FLASK_APP ?= app.py
GUNICORN_CMD_ARGS ?= --workers 3 --bind 0.0.0.0:8000 --timeout 120

.PHONY: run dev swagger console

run:
	GUNICORN_CMD_ARGS="$(GUNICORN_CMD_ARGS)" gunicorn $(APP_ENTRY)

dev:
	flask --app $(FLASK_APP) run --debug

swagger:
	@echo "Swagger UI at $${SWAGGER_UI_ROUTE:-/apidocs/}"

console:
	flask --app $(FLASK_APP) shell
