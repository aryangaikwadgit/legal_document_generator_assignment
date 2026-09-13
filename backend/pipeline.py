import os

from src.parser import PDFParser
from src.chunker import TextChunker
from src.extractor import CaseExtractor
from src.template_analyzer import TemplateAnalyzer
from src.mapper import ContentMapper
from src.generator import AffidavitGenerator
from src.document_builder import DocumentBuilder
from src.pdf_builder import PDFBuilder
from src.validators import AffidavitValidator
from src.evaluator import AffidavitEvaluator
from src.report_generator import EvaluationReportGenerator
from src.token_tracker import TokenTracker


class LegalDocumentGenerator:

    def __init__(
        self,
        case_pdf_path,
        format_pdf_path,
        sample_pdf_path,
        output_directory,
    ):
        self.case_pdf_path = case_pdf_path
        self.format_pdf_path = format_pdf_path
        self.sample_pdf_path = sample_pdf_path
        self.output_directory = output_directory

        self.token_tracker = TokenTracker()

        self.obj_parser = PDFParser(case_pdf_path)
        self.obj_chunker = TextChunker()
        self.obj_extractor = CaseExtractor(self.token_tracker)
        self.obj_template_analyzer = TemplateAnalyzer(self.token_tracker)
        self.obj_mapper = ContentMapper()
        self.obj_generator = AffidavitGenerator(self.token_tracker)
        self.obj_document_builder = DocumentBuilder()
        self.obj_pdf_builder = PDFBuilder()

    def generate(self):
        print("case extraction")

        text = self.obj_parser.extract_text()
        chunks = self.obj_chunker.create_chunks(text)

        extracted_data = self.obj_extractor.extract(chunks)

        print(extracted_data.model_dump_json(indent=4))

        print("template analysis")

        format_parser = PDFParser(self.format_pdf_path)
        sample_parser = PDFParser(self.sample_pdf_path)

        format_document = format_parser.extract_text()
        sample_document = sample_parser.extract_text()

        document_structure = self.obj_template_analyzer.analyze(format_document,sample_document)

        print(document_structure.model_dump_json(indent=4))

        print("mapping")

        mapped_content = self.obj_mapper.map_content(extracted_data,document_structure)

        print(mapped_content)

        print("document generation")

        generated_document = self.obj_generator.generate(mapped_content,document_structure)

        print(generated_document.model_dump_json(indent=4))

        print("file generation")

        os.makedirs(self.output_directory,exist_ok=True)

        affidavit_path = self.output_directory + r"\affidavit_in_reply.docx"

        self.obj_document_builder.build(generated_document)
        self.obj_document_builder.save(affidavit_path)

        pdf_path = self.output_directory + r"\affidavit_in_reply.pdf"

        self.obj_pdf_builder.build(generated_document,pdf_path)

        print(affidavit_path)
        print(pdf_path)

        print("validation")

        validator = AffidavitValidator(affidavit_path)

        validation_result = validator.validate(extracted_data)

        print(validation_result)

        print("evaluation")

        evaluator = AffidavitEvaluator()

        evaluation = evaluator.evaluate(extracted_data,validation_result)

        print(evaluation)

        print("report")

        report_generator = EvaluationReportGenerator()

        report_path = self.output_directory + r"\evaluation_report.json"

        report_generator.generate(evaluation,report_path)

        print(report_path)

        print("token usage")

        token_usage = self.token_tracker.summary()

        print(token_usage)

        return {
            "extracted_data": extracted_data,
            "document_structure": document_structure,
            "mapped_content": mapped_content,
            "generated_document": generated_document,
            "affidavit_path": affidavit_path,
            "pdf_path": pdf_path,
            "validation_result": validation_result,
            "evaluation": evaluation,
            "report_path": report_path,
        }


if __name__ == "__main__":

    base_directory = (
        r"C:\Main_Drive\work\workarea\projects"
        r"\Brainwonders\legal_document_generator_assignment")

    reference_directory = base_directory + r"\data\reference"

    output_directory = base_directory + r"\outputs"

    case_pdf_path = reference_directory + r"\03_Case_Information.pdf"

    format_pdf_path = reference_directory + r"\01 Affidavit Format Explained.pdf"

    sample_pdf_path = reference_directory + r"\02 Affidavit in Reply Sample.docx.pdf"

    obj_generator = LegalDocumentGenerator(
        case_pdf_path,
        format_pdf_path,
        sample_pdf_path,
        output_directory,
    )

    result = obj_generator.generate()
