import requests
import streamlit as st

st.title("Legal Document Generator")

case_pdf = st.file_uploader(
    "Upload Case Information PDF",
    type=["pdf"],
)

if st.button("Generate Document"):

    if case_pdf is None:
        st.warning("Please upload the Case Information PDF.")
    else:
        files = {
            "case_pdf": (
                case_pdf.name,
                case_pdf.getvalue(),
                "application/pdf",
            )
        }

        with st.spinner("Generating document..."):
            response = requests.post(
                "http://127.0.0.1:8000/generate",
                files=files,
            )

        if response.status_code == 200:

            result = response.json()

            st.success("Document generated successfully.")

            st.subheader("Entity Extraction")
            st.json(result["entities"])

            st.subheader("Content Mapping")
            st.json(result["mapping"])

            st.subheader("Evaluation")
            st.json(result["evaluation"])

            st.subheader("Generated Document")

            pdf_response = requests.get("http://127.0.0.1:8000/download/pdf")

            st.download_button(
                "Download Affidavit PDF",
                pdf_response.content,
                "affidavit_in_reply.pdf",
                "application/pdf",
            )

            docx_response = requests.get("http://127.0.0.1:8000/download/docx")

            st.download_button(
                "Download Affidavit DOCX",
                docx_response.content,
                "affidavit_in_reply.docx",
            )

            st.subheader("Evaluation Report")

            report_response = requests.get("http://127.0.0.1:8000/evaluation-report")

            st.download_button(
                "Download Evaluation Report",
                report_response.content,
                "evaluation_report.json",
                "application/json",
            )

        else:
            st.error("Document generation failed.")
