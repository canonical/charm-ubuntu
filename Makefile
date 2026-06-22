.PHONY: lint format unit integration

lint:
	uv run --group lint ruff check src tests
	uv run --group lint pyright src tests
	uv run --group lint ruff format --check src tests

format:
	uv run --group lint ruff check --fix src tests
	uv run --group lint ruff format src tests

unit:
	uv run --group unit pytest --tb native --show-capture=no --log-cli-level=INFO -s -W error tests/unit

integration:
	uv run --group integration pytest --tb native --show-capture=no --log-cli-level=INFO -s --disable-warnings --model-config tests/data/model-config.yaml tests/integration
