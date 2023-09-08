"""
Main Application Entry Point

This module serves as the main entry point for the Document Summarizer application.

Author: Mirza Bilal
"""

from frontend import DocumentSummarizerApp


def main():
    """
    Main entry point for the Document Summarizer application.
    Creates an instance of DocumentSummarizerApp and starts the main application loop.
    """
    app = DocumentSummarizerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
