import re

class TextChunker:

    def create_chunks(self, text):

        paragraphs = re.split(r"\n\s*\n", text)   # split the extracted text into paragraphs using blank lines

        chunks = []

        for paragraph in paragraphs:  #clean each paragraph and store non-empty paragraphs as chunks

            paragraph = paragraph.strip()

            if paragraph:
                chunks.append(paragraph)

        return chunks
