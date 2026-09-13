import os
import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from pipeline import LegalDocumentGenerator

app = FastAPI(title="Legal Document Generator")

BASE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REFERENCE_DIRECTORY = BASE_DIRECTORY + r"\data\reference"
OUTPUT_DIRECTORY = BASE_DIRECTORY + r"\outputs"

FORMAT_PDF_PATH = REFERENCE_DIRECTORY + r"\01 Affidavit Format Explained.pdf"
SAMPLE_PDF_PATH = REFERENCE_DIRECTORY + r"\02 Affidavit in Reply Sample.docx.pdf"


@app.post("/generate")
async def generate_document(case_pdf: UploadFile = File(...)):

    case_pdf_path = OUTPUT_DIRECTORY + r"\uploaded_case_information.pdf"

    os.makedirs(
        OUTPUT_DIRECTORY,
        exist_ok=True,
    )

    with open(case_pdf_path, "wb") as file:
        shutil.copyfileobj(
            case_pdf.file,
            file,
        )

    generator = LegalDocumentGenerator(
        case_pdf_path,
        FORMAT_PDF_PATH,
        SAMPLE_PDF_PATH,
        OUTPUT_DIRECTORY,
    )

    result = generator.generate()

    return {
        "message": "Legal document generated successfully",
        "entities": result["extracted_data"].model_dump(),
        "mapping": result["mapped_content"],
        "evaluation": result["evaluation"],
        "validation": result["validation_result"],
        "files": {
            "pdf": "/download/pdf",
            "docx": "/download/docx",
            "report": "/evaluation-report",
        },
    }


@app.get("/download/pdf")
def download_pdf():

    path = OUTPUT_DIRECTORY + r"\affidavit_in_reply.pdf"

    return FileResponse(
        path,
        filename="affidavit_in_reply.pdf",
        media_type="application/pdf",
    )


@app.get("/download/docx")
def download_docx():

    path = OUTPUT_DIRECTORY + r"\affidavit_in_reply.docx"

    return FileResponse(
        path,
        filename="affidavit_in_reply.docx",
        media_type=(
            "application/vnd.openxmlformats-officedocument" ".wordprocessingml.document"
        ),
    )


@app.get("/evaluation-report")
def evaluation_report():

    path = OUTPUT_DIRECTORY + r"\evaluation_report.json"

    return FileResponse(
        path,
        filename="evaluation_report.json",
        media_type="application/json",
    )
