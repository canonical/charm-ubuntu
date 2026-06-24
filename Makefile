.DEFAULT_GOAL := help

.PHONY: help lint format unit integration

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

lint:  ## Lint with ruff and type-check with pyright
	uv run --group lint ruff check src tests
	uv run --group lint --group unit --group integration pyright src tests
	uv run --group lint ruff format --check src tests

format:  ## Format and auto-fix with ruff
	uv run --group lint ruff check --fix src tests
	uv run --group lint ruff format src tests

unit:  ## Run unit tests
	uv run --group unit pytest --tb native --show-capture=no --log-cli-level=INFO -s -W error tests/unit

integration:  ## Run integration tests
	uv run --group integration pytest --tb native --show-capture=no --log-cli-level=INFO -s --disable-warnings --model-config tests/data/model-config.yaml tests/integration
