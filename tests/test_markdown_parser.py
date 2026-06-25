from pathlib import Path

from ingestion.parsers.markdown import MarkdownParser


def test_markdown_parser():

    parser = MarkdownParser()

    document = parser.parse(
        Path("D:\\memora-ai\\tests\\data\\sample.md")
    )

    print(document)

    assert document.title == "Memora AI"

    assert len(document.headings) == 3

    assert document.word_count > 0

    assert "Incremental Indexing" in document.text

    assert len(document.code_blocks) == 1

    assert len(document.links) == 1

    assert len(document.images) == 1