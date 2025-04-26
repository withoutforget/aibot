OS ?= $(shell uname -s)
ifeq ($(findstring NT,$(OS)),NT)
  OS_TYPE = Windows
  RM = rmdir /s /q
else ifeq ($(OS),Linux)
  OS_TYPE = Linux
  RM = rm -rf
else
  OS_TYPE = Other
endif

run:
	uv run -m src.main
init_dirs:
	mkdir logs
clean:
	uv run ruff clean
	uv run pyclean .
	uv clean
	$(RM) logs
depends:
	uv venv
	uv sync
	mkdir logs
format:
	uv run ruff format
check:
	uv run ruff check

all: depends check clean init_dirs run