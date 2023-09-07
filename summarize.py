"""
a
"""
from transformers import BartForConditionalGeneration, BartTokenizer

class BartSummarizer:
    """
    c
    """
    def __init__(self, model_name='facebook/bart-large-cnn'):
        """
        b
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None

    def init_model(self):
        """
        c
        """
        print("Initializing model")
        self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
        self.model = BartForConditionalGeneration.from_pretrained(self.model_name)
        print("Initializing model done")

    def summarize_text(self, text, min_length=30, max_length=150):
        """
        c
        """
        inputs = self.tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)

        # Set min_length and max_length
        summary_ids = self.model.generate(inputs.input_ids, num_beams=4, min_length=min_length,
                                          max_length=max_length, early_stopping=True)

        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary

