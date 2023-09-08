"""
Khulasa Document Summarization Classes

This module defines three classes: KhDocument, KhPage, and KhBlock, which are used for
document summarization.

Author: Mirza Bilal
"""


class KhDocument:
    """
    Represents a document for summarization.

    Attributes:
        pages (list): A list of KhPage objects representing the pages in the document.

    Methods:
        add_page(page_number): Add a new page to the document.
        get_text(): Retrieve the text content of the entire document.
    """

    def __init__(self):
        self.pages = []

    def add_page(self, page_number):
        """
        Add a new page to the document.

        Args:
            page_number (int): The page number to be added.

        Returns:
            KhPage: The newly added KhPage object.
        """
        page = KhPage(page_number)
        self.pages.append(page)
        return page

    def get_text(self):
        """
        Retrieve the text content of the entire document.

        Returns:
            str: The concatenated text content of all pages in the document.
        """
        return '\n'.join(page.get_text() for page in self.pages)


class KhPage:
    """
    Represents a page within a document.

    Attributes:
        page_number (int): The page number.
        blocks (list): A list of KhBlock objects representing the text blocks on the page.

    Methods:
        add_block(block_text): Add a new text block to the page.
        get_text(): Retrieve the text content of the page.
    """

    def __init__(self, page_number):
        self.page_number = page_number
        self.blocks = []

    def add_block(self, block_text):
        """
        Add a new text block to the page.

        Args:
            block_text (str): The text content of the block to be added.
        """
        block = KhBlock(block_text)
        self.blocks.append(block)

    def get_text(self):
        """
        Retrieve the text content of the page.

        Returns:
            str: The concatenated text content of all blocks on the page.
        """
        return ' '.join(block.text for block in self.blocks)


class KhBlock:
    """
    Represents a text block within a page.

    Attributes:
        text (str): The text content of the block.

    Methods:
        None
    """

    def __init__(self, text):
        self.text = text
