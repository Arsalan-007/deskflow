.PHONY: install lint test eval run inspector

install:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -e ".[dev]"

lint:
	.venv/bin/ruff check src tests

test:
	.venv/bin/pytest -q --cov=src

eval:
	.venv/bin/python -m eval.evaluate

run:
	.venv/bin/python -m agent.run_digest

inspector:
	npx @modelcontextprotocol/inspector .venv/bin/python -m mcp_server.server
