"""
    HELLO
"""
from threading import Thread
import tkinter as tk
from tkinter import filedialog
from customtkinter import CTk, CTkEntry, \
    CTkButton, CTkLabel, CTkTextbox, CTkProgressBar
from text_extractor import TextExtractor
from summarize import BartSummarizer

class DocumentSummarizerApp(CTk):
    """
    DocumentSummarizerApp
    """

    def __init__(self):
        super().__init__()
        # Example usage:
        self.summarizer = BartSummarizer()
        self.model_initialized = False

        self.text_extractor = TextExtractor()
        # configure window
        self.title("Khulasa - Text Extractor and Summarizer")
        self.geometry(f"{840}x{600}")
        self.resizable(0,0)

        self.columnconfigure(2, weight=1)

        self.rowconfigure(2, weight=1)

        self.pdf_entry = CTkEntry(self, placeholder_text="Select pdf or docx",
                                   height=24, width=220)
        self.pdf_entry.grid(row=0, column=0, columnspan=1, padx=(20, 0),
                            pady=(20, 0), sticky=tk.NSEW)

        self.select_button = CTkButton(master=self, text="Select Document", height=24,
                                       border_width=0, text_color="white",
                                       command=self.open_file_dialog, state="disabled")
        self.select_button.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky=tk.NSEW)

        self.summary_label = CTkLabel(master=self, text="Summary:", height=10)
        self.summary_label.grid(row=1, column=0, columnspan=1, padx=20, pady=20, sticky="w")

        self.summary_textbox = CTkTextbox(self)
        self.summary_textbox.grid(row=2, column=0, columnspan=2, padx=(20, 20),
                                  pady=(0, 20), sticky=tk.NSEW)

        self.text_label = CTkLabel(master=self, text="Text:", height=10)
        self.text_label.grid(row=0, column=2, columnspan=1, padx=20, pady=20, sticky="w")

        self.textbox = CTkTextbox(self, width=300, state='disabled')
        self.textbox.grid(row=1, column=2, rowspan=2, columnspan=2, padx=(20, 20),
                          pady=(0, 20), sticky=tk.NSEW)

        self.progressbar = CTkProgressBar(self)
        self.progressbar.grid(row=0, columnspan=1, column=3, padx=(20, 20), sticky="ew")
        self.progressbar.configure(mode="indeterminnate")
        # self.progressbar.start()
        self.init_model()

    def summarize_document(self):
        """
        a
        """
        text = self.textbox.get("1.0", "end-1c")
        def background_summarization():
            self.text_label.configure(text="Generating Summary")
            self.progressbar.grid(row=0, columnspan=1, column=3, padx=(20, 20), sticky="ew")
            self.progressbar.start()
            summary = self.summarizer.summarize_text(text, 100, 500)
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
        a
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
        a
        """
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"),
                                                          ("Word files", "*.docx")])
        if file_path:
            print("File: ", file_path)
            result = self.text_extractor.parse_file(file_path)
            print("Got the result, ", result.get_text())
            self.textbox.configure(state='normal')
            self.summary_textbox.delete("1.0", tk.END)
            self.textbox.insert(1.0, result.get_text())
            self.textbox.configure(state='disabled')
            self.summarize_document()
