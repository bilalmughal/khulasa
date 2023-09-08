"""
Text Summarization Classes

This module defines two text summarization classes: BartSummarizer and AbstractiveSummarizer.

Author: Mirza Bilal
"""

from transformers import BartForConditionalGeneration, BartTokenizer


class BartSummarizer:
    """
    A text summarization class using the BART model.

    Attributes:
        model_name (str): The name of the BART model to use (default is 'facebook/bart-large-cnn').
        tokenizer: The BART tokenizer.
        model: The BART model for summarization.

    Methods:
        __init__(model_name='facebook/bart-large-cnn'): Initializes the BartSummarizer.
        init_model(): Initializes the BART model and tokenizer.
        summarize_text(text, length=150): Summarizes the input text using the BART model.
    """

    def __init__(self, model_name='facebook/bart-large-cnn'):
        """
        Initializes the BartSummarizer.

        :param model_name: The name of the BART model to use (default is 'facebook/bart-large-cnn').
        """
        self.model_name = model_name
        self.tokenizer = None
        self.model = None

    def init_model(self):
        """
        Initializes the BART model and tokenizer.
        """
        print("Initializing model")
        self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
        self.model = BartForConditionalGeneration.from_pretrained(
            self.model_name)
        print("Initializing model done")

    def summarize_text(self, text, max_summary_length=512):
        """
        Summarizes the input text using the BART model.

        :param text: The input text to summarize.
        :param max_summary_length: The maximum length of the summary (default is 512 tokens).

        :return: The summarized text.
        """
        if self.tokenizer is not None and len(text) > self.tokenizer.model_max_length:
            # Text exceeds the maximum token limit, split it into segments
            segments = []
            remaining_text = text

            while len(remaining_text) > 0:
                # Determine the segment length, considering the model's token limit
                segment_length = self.tokenizer.model_max_length

                # Find a suitable split point within the segment_length
                split_point = remaining_text.rfind(" ", 0, segment_length)
                if split_point <= 0:
                    split_point = segment_length  # If no space found, split at the segment_length

                # Extract a segment
                segment, remaining_text = remaining_text[:split_point],\
                    remaining_text[split_point:].strip()
                segments.append(segment)

            print("Number of segments: ", len(segments))
            selected_segments = []
            selected_segments = segments if len(
                segments) <= 3 else segments[:3]
            # Generate summaries for each segment
            summaries = []
            for segment in selected_segments:
                summary = self._summarize_segment(segment, max_summary_length)
                summaries.append(summary)

            # Combine the summaries
            combined_summary = " ".join(summaries)
            return combined_summary
        else:
            # Text does not exceed the maximum token limit, summarize it directly
            summary = self._summarize_segment(text, max_summary_length)
            return summary

    def _summarize_segment(self, text, max_summary_length):
        """
        Generates summaries for a text.

        :param text: Text to be summarize.
        :param max_summary_length: The maximum length of the summary.

        :return: The combined summarized text.
        """
        if isinstance(self.tokenizer, BartTokenizer) and \
            isinstance(self.model, BartForConditionalGeneration):
            inputs = self.tokenizer(
                [text], max_length=self.tokenizer.model_max_length,
                return_tensors='pt', truncation=True)
            summary_ids = self.model.generate(
                inputs.input_ids, num_beams=4, min_length=30,
                max_length=max_summary_length, early_stopping=True)
            summary = self.tokenizer.decode(
                summary_ids[0], skip_special_tokens=True)
            return summary
        return ""
