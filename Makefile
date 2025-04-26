run:
	uv run -m src.main
clean:
	uv clean
depends:
	uv venv
	uv sync

ldepends: depends

lrun: run

