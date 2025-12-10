from formdt import format_markdown, Config


class TestLineWrapping:
    def test_wraps_long_line_at_configured_length(self):
        config = Config(line_length=40)
        text = "This is a long line that should be wrapped at forty characters."
        result = format_markdown(text, config)

        lines = result.split("\n")
        for line in lines:
            assert len(line) <= 40

    def test_preserves_short_lines(self):
        config = Config(line_length=80)
        text = "Short line."
        result = format_markdown(text, config)

        assert result == "Short line."

    def test_joins_single_line_breaks(self):
        config = Config(line_length=80)
        text = "Line one\nLine two\nLine three"
        result = format_markdown(text, config)

        assert result == "Line one Line two Line three"

    def test_preserves_double_line_breaks_as_paragraphs(self):
        config = Config(line_length=80)
        text = "Paragraph one.\n\nParagraph two."
        result = format_markdown(text, config)

        assert result == "Paragraph one.\n\nParagraph two."

    def test_wraps_each_paragraph_independently(self):
        config = Config(line_length=30)
        text = (
            "This is the first paragraph with words.\n\nThis is the second paragraph."
        )
        result = format_markdown(text, config)

        paragraphs = result.split("\n\n")
        assert len(paragraphs) == 2
        for para in paragraphs:
            for line in para.split("\n"):
                assert len(line) <= 30

    def test_handles_empty_string(self):
        config = Config(line_length=80)
        result = format_markdown("", config)

        assert result == ""

    def test_handles_multiple_consecutive_paragraphs(self):
        config = Config(line_length=80)
        text = "One.\n\nTwo.\n\nThree."
        result = format_markdown(text, config)

        assert result == "One.\n\nTwo.\n\nThree."

    def test_word_longer_than_line_length_stays_on_own_line(self):
        config = Config(line_length=10)
        text = "Short verylongwordhere end"
        result = format_markdown(text, config)

        lines = result.split("\n")
        assert "verylongwordhere" in lines[1]

    def test_default_config_uses_80_chars(self):
        config = Config()
        assert config.line_length == 80

    def test_format_without_config_uses_defaults(self):
        text = "Short text"
        result = format_markdown(text)

        assert result == "Short text"


class TestCallouts:
    def test_wraps_callout_with_prefix_on_continuation_lines(self):
        config = Config(line_length=40)
        text = "> You must specify either `-m` (all markdown cells) or `-c` (specific cells) when formatting notebooks."
        result = format_markdown(text, config)

        lines = result.split("\n")
        assert len(lines) > 1
        for line in lines:
            assert line.startswith(">")
            assert len(line) <= 40

    def test_preserves_short_callout(self):
        config = Config(line_length=80)
        text = "> Short callout."
        result = format_markdown(text, config)

        assert result == "> Short callout."

    def test_nested_callout_prefix_preserved(self):
        config = Config(line_length=30)
        text = ">> This is a nested callout that should wrap properly."
        result = format_markdown(text, config)

        lines = result.split("\n")
        for line in lines:
            assert line.startswith(">>")

    def test_github_admonition_stays_on_own_line(self):
        config = Config(line_length=80)
        text = "> [!note]\n> You must specify either `-m` (all markdown cells) or `-c` (specific cells) when formatting notebooks."
        result = format_markdown(text, config)

        lines = result.split("\n")
        assert lines[0] == "> [!note]"
        assert all(line.startswith(">") for line in lines)

    def test_github_admonition_with_text_on_same_line(self):
        config = Config(line_length=80)
        text = "> [!warning] This is a warning that should stay on its own line.\n> More content here."
        result = format_markdown(text, config)

        lines = result.split("\n")
        assert lines[0].startswith("> [!warning]")
        assert "[!warning]" not in lines[1]
