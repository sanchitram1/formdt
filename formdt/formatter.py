import re
from .config import Config

LINK_PATTERN = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')


def format_markdown(text: str, config: Config | None = None) -> str:
    if config is None:
        config = Config()
    
    paragraphs = text.split("\n\n")
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        formatted_paragraphs.append(_wrap_paragraph(paragraph, config.line_length))
    
    return "\n\n".join(formatted_paragraphs)


def _wrap_paragraph(paragraph: str, line_length: int) -> str:
    lines = paragraph.split("\n")
    combined = " ".join(lines)
    
    if not combined.strip():
        return ""
    
    tokens = _tokenize_with_links(combined)
    
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
        before = text[last_end:match.start()]
        if before:
            tokens.extend(before.split())
        tokens.append(match.group(0))
        last_end = match.end()
    
    after = text[last_end:]
    if after:
        tokens.extend(after.split())
    
    return tokens
