up:
	docker compose up
build:
	docker compose build
down:
	docker compose down
migrate ARGS='':
	docker compose run --rm aurochs bash -c 'python manage.py migrate {{ARGS}}'
makemigrations ARGS='':
	docker compose run --rm aurochs bash -c 'python manage.py makemigrations {{ARGS}}'
restart:
	docker compose restart aurochs
shell ARGS='':
	docker compose run --rm aurochs bash -c 'python manage.py shell {{ARGS}}'
manage ARGS='':
	docker compose run --rm aurochs bash -c 'python manage.py {{ARGS}}'
bash:
	docker compose run --rm aurochs bash
rebuild_index ARGS='':
	docker compose run --rm aurochs bash -c 'python manage.py update_index {{ARGS}}'
test ARGS='':
	docker compose run --rm aurochs bash -c 'python manage.py test {{ARGS}}'
pip_update:
	docker compose run --rm aurochs bash -c 'pip install --upgrade pip && pip install -r requirements.unstable.txt && pip freeze -r requirements.unstable.txt > requirements.txt && cat requirements.txt'
lint:
	black aurochs && flake8 .

# E2E Testing Commands
e2e-setup:
	docker compose run --rm aurochs bash -c 'python manage.py setup_e2e_accounts'

e2e-clean:
	docker compose run --rm aurochs bash -c 'python manage.py clear_e2e_data'

e2e-open: e2e-setup
	@echo "Starting Cypress interactive mode..."
	@echo "Make sure docker compose up is running in another terminal!"
	npx cypress open

e2e SPEC='': e2e-setup
	@echo "Running Cypress E2E tests..."
	@echo "Make sure docker compose up is running!"
	npx cypress run{{if SPEC != '' { ' --spec "' + SPEC + '"' } else { '' } }}

e2e-csrf: e2e-setup
	@echo "Running CSRF endpoint tests..."
	npx cypress run --spec "cypress/e2e/csrf_endpoint_tests.js"

e2e-headless SPEC='': e2e-setup
	@echo "Running Cypress tests in headless mode..."
	npx cypress run --headless{{if SPEC != '' { ' --spec "' + SPEC + '"' } else { '' } }}