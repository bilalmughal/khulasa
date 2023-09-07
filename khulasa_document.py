"""
Doc
"""


class KhDocument:
    def __init__(self):
        self.pages = []

    def add_page(self, page_number):
        page = KhPage(page_number)
        self.pages.append(page)
        return page

    def get_text(self):
        return '\n'.join(page.get_text() for page in self.pages)


class KhPage:
    def __init__(self, page_number):
        self.page_number = page_number
        self.blocks = []

    def add_block(self, block_text):
        block = KhBlock(block_text)
        self.blocks.append(block)

    def get_text(self):
        return ' '.join(block.text for block in self.blocks)


class KhBlock:
    def __init__(self, text):
        self.text = text
