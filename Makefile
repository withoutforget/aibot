run:
	uv run -m src.main
clean:
	uv clean
depends:
	uv venv
	uv sync
format:
	uv run ruff format
check:
	uv run ruff check
ldepends: depends

lrun: run
