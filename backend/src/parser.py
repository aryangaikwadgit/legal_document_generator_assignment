import fitz


class PDFParser:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):

        doc = fitz.open(self.pdf_path)  #open the PDF document

        text = ""

        #extract text from each page
        
        for page in doc:
            text += page.get_text()

        #close the PDF document
        doc.close()

        return text.strip()
