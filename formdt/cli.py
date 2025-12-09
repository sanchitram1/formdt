import argparse
import sys
from pathlib import Path

from .config import load_config
from .formatter import format_markdown


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="formdt",
        description="Format markdown files with configurable line length"
    )
    parser.add_argument("file", type=Path, help="Markdown file to format")
    parser.add_argument(
        "-l", "--line-length",
        type=int,
        help="Override line length (default: from .formdt or 80)"
    )
    parser.add_argument(
        "-w", "--write",
        action="store_true",
        help="Write changes back to file (default: print to stdout)"
    )
    
    args = parser.parse_args()
    
    config = load_config()
    if args.line_length:
        config.line_length = args.line_length
    
    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1
    
    content = args.file.read_text()
    formatted = format_markdown(content, config)
    
    if args.write:
        args.file.write_text(formatted)
    else:
        print(formatted)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
