# formdt

A markdown formatter with configurable line length, supporting
both `.md` files and Jupyter notebooks.

## Commands

```bash
# Run tests
uv run pytest -v

# Format code (required before committing)
uv run ruff format .

# Lint code (required before committing)
uv run ruff check . --fix

# Build package
uv build

# Run the CLI
uv run formdt <file> [options]
```

## Project Structure

- `formdt/formatter.py` - Core markdown formatting logic with link preservation
- `formdt/notebook.py` - Jupyter notebook parsing and formatting
- `formdt/cli.py` - Command-line interface
- `formdt/config.py` - Configuration loading from `.formdt` file
- `tests/` - pytest tests

## Key Conventions

- Links `[text](url)` are treated as atomic tokens and never broken across lines
- Default line length is 80 characters
- Config file is `.formdt` in working directory with `line_length = N` format
- Notebooks use 0-indexed cell numbers

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit and push
4. Tag with `git tag vX.Y.Z && git push origin vX.Y.Z`
5. GitHub Actions publishes to PyPI via trusted publishing
