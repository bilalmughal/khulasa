import fitz
from docx import Document
from khulasa_document import KhDocument

class TextExtractor:
    """
    a
    """
    def __init__(self):
        pass

    def parse_file(self, file_path):
        """
        a
        """
        file_extension = file_path.split(".")[-1].lower()  # Extract and convert to lowercase

        # Check the file extension
        if file_extension == "pdf":
            return self._parse_pdf(file_path)

        elif file_extension == "docx":
            print("This is a DOCX file.")
            return self._parse_docx(file_path)
        else:
            print("Unsupported file format.")
            return None


    def _parse_pdf(self, pdf_path):
        pdf = fitz.open(pdf_path)
        document = KhDocument()
        current_page = None  # Initialize to None

        for page_number, page in enumerate(pdf, start=1):
            # Get text blocks
            blocks = page.get_text("blocks")

            for block in blocks:
                if '<image:' not in block[4]:
                    if current_page is None or current_page.page_number != page_number:
                        current_page = document.add_page(page_number)
                    current_page.add_block(block[4])
        return document

    def _parse_docx(self, docx_file):
        document = Document(docx_file)
        kh_document = KhDocument()
        current_page = None

        for paragraph in document.paragraphs:
            if current_page is None:
                # Create a new page at the beginning of the document
                page_number = len(kh_document.pages) + 1
                current_page = kh_document.add_page(page_number)

            # Check if the paragraph represents a page break
            if paragraph.style.name == 'PageBreak':
                # Create a new page
                page_number = len(kh_document.pages) + 1
                current_page = kh_document.add_page(page_number)
            else:
                # Add the paragraph text as a block to the current page
                current_page.add_block(paragraph.text)

        return kh_document
    