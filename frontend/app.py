import os
import sys

import streamlit as st

os.environ["OLLAMA_API_KEY"] = st.secrets["OLLAMA_API_KEY"]
os.environ["OLLAMA_MODEL"] = st.secrets["OLLAMA_MODEL"]

base_directory = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, base_directory)
sys.path.insert(0, base_directory + "/backend")

from backend.pipeline import LegalDocumentGenerator"

st.title("Legal Document Generator")

case_pdf = st.file_uploader(
    "Upload Case Information PDF",
    type=["pdf"],
)

if st.button("Generate Document"):

    if case_pdf is None:
        st.warning("Please upload the Case Information PDF.")
    else:
        case_pdf_path = base_directory + "/outputs/uploaded_case_information.pdf"

        format_pdf_path = (
            base_directory + "/data/reference/01 Affidavit Format Explained.pdf"
        )

        sample_pdf_path = (
            base_directory + "/data/reference/02 Affidavit in Reply Sample.docx.pdf"
        )

        output_directory = base_directory + "/outputs"

        os.makedirs(
            output_directory,
            exist_ok=True,
        )

        with open(case_pdf_path, "wb") as file:
            file.write(case_pdf.getvalue())

        with st.spinner("Generating document..."):

            generator = LegalDocumentGenerator(
                case_pdf_path,
                format_pdf_path,
                sample_pdf_path,
                output_directory,
            )

            result = generator.generate()

        st.success("Document generated successfully.")

        st.subheader("Entity Extraction")
        st.json(result["extracted_data"].model_dump())

        st.subheader("Content Mapping")
        st.json(result["mapped_content"])

        st.subheader("Evaluation")
        st.json(result["evaluation"])

        st.subheader("Generated Document")

        with open(
            result["pdf_path"],
            "rb",
        ) as file:

            st.download_button(
                "Download Affidavit PDF",
                file,
                "affidavit_in_reply.pdf",
                "application/pdf",
            )

        with open(
            result["affidavit_path"],
            "rb",
        ) as file:

            st.download_button(
                "Download Affidavit DOCX",
                file,
                "affidavit_in_reply.docx",
            )

        st.subheader("Evaluation Report")

        with open(
            result["report_path"],
            "rb",
        ) as file:

            st.download_button(
                "Download Evaluation Report",
                file,
                "evaluation_report.json",
                "application/json",
            )
