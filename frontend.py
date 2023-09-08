"""
Document Summarizer App

This module defines the DocumentSummarizerApp class, which is a GUI application
for text extraction and summarization.

Author: Mirza Bilal
"""

from threading import Thread
import tkinter as tk
from tkinter import filedialog
from customtkinter import CTk, CTkEntry, \
    CTkButton, CTkLabel, CTkTextbox, CTkProgressBar
from text_extractor import TextExtractor
from summarize import BartSummarizer
# from summarize import AbstractiveSummarizer


class DocumentSummarizerApp(CTk):
    """
    DocumentSummarizerApp class for text extraction and summarization.

    Attributes:
        summarizer: An instance of the summarization model (e.g., BartSummarizer).
        model_initialized (bool): A flag indicating whether the summarization model is initialized.
        text_extractor: An instance of the text extraction tool.

    Methods:
        __init__(): Initializes the GUI application.
        summarize_document(): Initiates the summarization process.
        init_model(): Initializes the summarization model in the background.
        open_file_dialog(): Opens a file dialog for selecting a PDF or DOCX document.
    """

    def __init__(self):
        """
        Initialize the DocumentSummarizerApp.
        """
        super().__init__()
        # Example usage:
        # self.summarizer = BartSummarizer()
        self.summarizer = BartSummarizer()
        self.model_initialized = False

        self.text_extractor = TextExtractor()
        # configure window
        self.title("Khulasa - Text Extractor and Summarizer")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set the window size and position to center it
        window_width = 840
        window_height = 600
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        self.geometry(
            f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        self.resizable(False, False)

        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(2, weight=1)

        self.rowconfigure(2, weight=1)

        self.document_path = CTkEntry(self, placeholder_text="Select pdf or docx",
                                      height=24, width=220)
        self.document_path.grid(row=0, column=0, columnspan=1, padx=(20, 0),
                                pady=(20, 0), sticky=tk.NSEW)

        self.select_button = CTkButton(master=self, text="Select Document", height=24,
                                       border_width=0, text_color="white",
                                       command=self.open_file_dialog, state="disabled")
        self.select_button.grid(row=0, column=1, padx=(
            20, 20), pady=(20, 0), sticky=tk.NSEW)

        self.summary_label = CTkLabel(master=self, text="Summary:", height=10)
        self.summary_label.grid(
            row=1, column=0, columnspan=1, padx=20, pady=20, sticky="w")

        self.summary_textbox = CTkTextbox(self, wrap="word")
        self.summary_textbox.grid(row=2, column=0, columnspan=2, padx=(20, 20),
                                  pady=(0, 20), sticky=tk.NSEW)

        self.text_label = CTkLabel(master=self, text="Text:", height=10)
        self.text_label.grid(row=0, column=2, columnspan=1,
                             padx=20, pady=20, sticky="w")

        self.textbox = CTkTextbox(
            self, width=300, state='disabled', wrap="word")
        self.textbox.grid(row=1, column=2, rowspan=2, columnspan=2, padx=(20, 20),
                          pady=(0, 20), sticky=tk.NSEW)

        self.progressbar = CTkProgressBar(self)
        self.progressbar.grid(row=0, columnspan=1, column=3,
                              padx=(20, 20), sticky="ew")
        self.progressbar.configure(mode="indeterminnate")
        # self.progressbar.start()
        self.init_model()

    def summarize_document(self):
        """
        Summarize the document.

        This method initiates the summarization process, running it in a separate thread.
        """
        text = self.textbox.get("1.0", "end-1c")

        def background_summarization():
            self.text_label.configure(text="Generating Summary")
            self.progressbar.grid(row=0, columnspan=1,
                                  column=3, padx=(20, 20), sticky="ew")
            self.progressbar.start()
            summary = self.summarizer.summarize_text(text, 512)
            self.progressbar.stop()
            self.progressbar.grid_forget()
            self.summary_textbox.delete("1.0", tk.END)
            self.summary_textbox.insert("1.0", summary)
            self.text_label.configure(text="Text:")

        # Create a separate thread for summarization
        summarization_thread = Thread(target=background_summarization)
        summarization_thread.start()

    def init_model(self):
        """
        Initialize the summarization model.

        This method initializes the summarization model in the background,
        running it in a separate thread.
        """
        def init_model_background():
            """
            a
            """
            self.text_label.configure(text="Initializing model")
            self.progressbar.start()
            self.summarizer.init_model()
            self.progressbar.stop()
            self.progressbar.grid_forget()
            self.model_initialized = True
            self.select_button.configure(state='normal')
            self.text_label.configure(text="Text:")
        self.init_model_thread = Thread(target=init_model_background)
        self.init_model_thread.start()

    def open_file_dialog(self):
        """
        Open a file dialog for selecting a PDF or DOCX document.

        This method allows the user to select a document for text extraction and summarization.
        """
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"),
                                                          ("Word files", "*.docx")])
        if file_path:
            print("File: ", file_path)
            self.document_path.insert(0, file_path)
            result = self.text_extractor.parse_file(file_path)
            self.textbox.configure(state='normal')
            self.textbox.delete("1.0", tk.END)
            text = result.get_text() if result is not None else "No text available"
            self.textbox.insert(1.0, text)
            self.textbox.configure(state='disabled')
            if result is not None:
                self.summarize_document()
