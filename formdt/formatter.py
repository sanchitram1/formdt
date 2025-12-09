import re

from .config import Config

LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
LIST_PATTERN = re.compile(r"^(\s*)([-*+]|\d+\.)\s")
HEADING_PATTERN = re.compile(r"^#{1,6}\s")
CODE_FENCE_PATTERN = re.compile(r"^```")
MATH_BLOCK_PATTERN = re.compile(r"^\$\$")


def format_markdown(text: str, config: Config | None = None) -> str:
    if config is None:
        config = Config()

    lines = text.split("\n")
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if CODE_FENCE_PATTERN.match(line):
            result.append(line)
            i += 1
            while i < len(lines) and not CODE_FENCE_PATTERN.match(lines[i]):
                result.append(lines[i])
                i += 1
            if i < len(lines):
                result.append(lines[i])
                i += 1
            continue

        if MATH_BLOCK_PATTERN.match(line.strip()):
            result.append(line)
            i += 1
            while i < len(lines) and not MATH_BLOCK_PATTERN.match(lines[i].strip()):
                result.append(lines[i])
                i += 1
            if i < len(lines):
                result.append(lines[i])
                i += 1
            continue

        if (
            HEADING_PATTERN.match(line)
            or LIST_PATTERN.match(line)
            or line.strip() == ""
        ):
            result.append(line)
            i += 1
            continue

        para_lines = [line]
        i += 1
        while i < len(lines):
            next_line = lines[i]
            if (
                next_line.strip() == ""
                or HEADING_PATTERN.match(next_line)
                or LIST_PATTERN.match(next_line)
                or CODE_FENCE_PATTERN.match(next_line)
                or MATH_BLOCK_PATTERN.match(next_line.strip())
            ):
                break
            para_lines.append(next_line)
            i += 1

        paragraph = " ".join(para_lines)
        wrapped = _wrap_paragraph(paragraph, config.line_length)
        result.append(wrapped)

    return "\n".join(result)


def _wrap_paragraph(paragraph: str, line_length: int) -> str:
    tokens = _tokenize_with_links(paragraph)

    if not tokens:
        return ""

    wrapped_lines = []
    current_line = []
    current_length = 0

    for token in tokens:
        token_length = len(token)

        if current_length == 0:
            current_line.append(token)
            current_length = token_length
        elif current_length + 1 + token_length <= line_length:
            current_line.append(token)
            current_length += 1 + token_length
        else:
            wrapped_lines.append(" ".join(current_line))
            current_line = [token]
            current_length = token_length

    if current_line:
        wrapped_lines.append(" ".join(current_line))

    return "\n".join(wrapped_lines)


def _tokenize_with_links(text: str) -> list[str]:
    tokens = []
    last_end = 0

    for match in LINK_PATTERN.finditer(text):
        before = text[last_end : match.start()]
        if before:
            tokens.extend(before.split())
        tokens.append(match.group(0))
        last_end = match.end()

    after = text[last_end:]
    if after:
        tokens.extend(after.split())

    return tokens
