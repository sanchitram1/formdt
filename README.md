# formdt

Markdown formatter with configurable line length.

## Installation

```bash
uv add formdt
```

## Usage

### CLI

```bash
# Print formatted output to stdout
formdt README.md

# Write changes back to file
formdt README.md --write

# Override line length
formdt README.md --line-length 120
```

### Library

```python
from formdt import format_markdown, Config

text = "This is a very long line that needs to be wrapped."
config = Config(line_length=40)

formatted = format_markdown(text, config)
```

## Configuration

Create a `.formdt` file in your project root:

```json
{
    "line_length": 80
}
```

## Rules

- **Line wrapping**: Lines are wrapped at the configured length (default: 80)
- **Single line breaks**: Joined within paragraphs (markdown treats them as spaces)
- **Double line breaks**: Preserved as paragraph separators

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest
```
