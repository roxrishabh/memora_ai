from ingestion.parsers.markdown import MarkdownParser


class ParserRegistry:

    def __init__(self):

        self.parsers = {
            ".md": MarkdownParser(),
            ".pdf": PDFParser(),
        }

    def get_parser(self, extension: str):

        return self.parsers.get(extension)