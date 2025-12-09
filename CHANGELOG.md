# Changelog

## [0.2.0] - 2024-12-08

### Added
- Jupyter notebook support with `-m` flag to format all markdown cells
- Cell selection with `-c` flag (e.g., `-c "0,2,5"` or `-c "1-3,7"`)
- Link preservation: `[text](url)` patterns are kept intact during wrapping

## [0.1.0] - 2024-12-08

### Added
- Initial release
- Markdown line wrapping with configurable line length
- `.formdt` config file support
- CLI with `-l` (line length) and `-w` (write) flags
