# Образец
SRC_PATH ?= SRC_PATH

.PHONY: install-dev-deps
install-dev-deps: install-deps
  pip install requirements.txt dev-requirements.txt

.PHONY: install-deps
install-deps:
  pip install requirements.txt

.PHONY: fmt
fmt:
  cd ${SRC_PATH} && autoflake .
  cd ${SRC_PATH} && isort .
  cd ${SRC_PATH} && black .

.PHONY: lint
lint:
  cd ${SRC_PATH} && python3 manage.py check
  cd ${SRC_PATH} && flake8
  cd ${SRC_PATH} && mypy

report_directory:
   mkdir -p ".reports"

.PHONY: test
test: report_directory
   mkdir -p ${SRC_PATH}/static ${SRC_PATH}/locale
   cd ${SRC_PATH} && python3 manage.py makemigrations --dry-run --no-input --check
   cd ${SRC_PATH} && python3 manage.py compilenessages
   cd ${SRC_PATH} && pytest --maxfail=5 -m "not slow" --junitxml=../.reports/xunit.xml --cov=. --cov-report xml:../.reports/coverage.xml

.PHONY: test-no-db
test-no-db: report_directory
   cd ${SRC_PATH} && pytest -m "not django_db" -m "not slow" --junitxml=../.reports/xunit.xml --cov=. --cov-report xml:../.reports/coverage.xml --disable-warnings -vvv

.PHONY: test-scenario
test-scenario: report_directory
   cd ${SRC_PATH} && pytest -m "slow" --junitxml=../.reports/xunit.xml --cov=. --cov-report xml:../.reports/coverage.xml --disable-warnings -vvv

.PHONY: venv-prepare
venv-prepare:
   python -m venv venv
   source venv/bin/activate
   pip install requirements.txt

.PHONY: venv-dev
venv-dev:
   venv-prepare
   pip install dev-requirements.txt

.PHONY: create-proto
create-proto:
   mkdir -p ${SRC_PATH}/protolib/iam_area
   cd ${SRC_PATH}/protolib && python -m grpc_tools.protoc -I=../../proto --python_betterproto_out=iam_area ../../proto/.../area_service.proto

.PHONY: create-reflection
create-reflection:
   mkdir -p ${SRC_PATH}/protolib/quota_reflection
   cd ${SRC_PATH}/protolib && python -m grpc_tools.protoc -I=../../proto --python_out=quota_reflection ../../proto/.../quota.proto

