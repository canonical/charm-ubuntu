.DEFAULT_GOAL := help

.PHONY: help lint format unit integration integration-debug

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

lint:  ## Lint with ruff and type-check with pyright
	uv run --locked --group lint ruff check
	uv run --locked --group lint --group unit --group integration pyright
	uv run --locked --group lint ruff format --check

format:  ## Format and auto-fix with ruff
	uv run --group lint ruff check --fix
	uv run --group lint ruff format

unit:  ## Run unit tests
	uv run --locked --group unit pytest --tb native --show-capture=no --log-cli-level=INFO -s tests/unit

integration:  ## Run integration tests via opcli/spread
	uv run --locked --group tooling opcli spread run

integration-debug:  ## Run integration tests via opcli/spread, dropping into a shell on failure
	uv run --locked --group tooling opcli spread run -- -debug
