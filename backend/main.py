from src.parser import PDFParser
from src.chunker import TextChunker
from src.extractor import CaseExtractor


class LegalDocumentGenerator:

    def __init__(self, pdf_path):
        self.obj_parser = PDFParser(pdf_path)
        self.obj_chunker = TextChunker()
        self.obj_extractor = CaseExtractor()

    def generate(self):

        # Step 1: Extract text from the PDF
        text = self.obj_parser.extract_text()

        # Step 2: Create chunks from the extracted text
        chunks = self.obj_chunker.create_chunks(text)

        # Step 3: Extract case information from the chunks
        extracted_data = self.obj_extractor.extract(chunks)

        return extracted_data


if __name__ == "__main__":

    pdf_path = r"C:\Main_Drive\work\workarea\projects\Brainwonders\legal_document_generator_assignment\data\reference\03_Case_Information.pdf"

    obj_generator = LegalDocumentGenerator(pdf_path)

    extracted_data = obj_generator.generate()

    print("\n--- Extracted Data ---")
    print(extracted_data[0].model_dump_json(indent=4))