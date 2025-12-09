from .config import Config


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
    words = " ".join(lines).split()
    
    if not words:
        return ""
    
    wrapped_lines = []
    current_line = []
    current_length = 0
    
    for word in words:
        word_length = len(word)
        
        if current_length == 0:
            current_line.append(word)
            current_length = word_length
        elif current_length + 1 + word_length <= line_length:
            current_line.append(word)
            current_length += 1 + word_length
        else:
            wrapped_lines.append(" ".join(current_line))
            current_line = [word]
            current_length = word_length
    
    if current_line:
        wrapped_lines.append(" ".join(current_line))
    
    return "\n".join(wrapped_lines)
