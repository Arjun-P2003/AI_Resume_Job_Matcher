
import pymupdf


def extract_resume_text(pdf_file):

    try:
        pdf_document = pymupdf.open(
            stream=pdf_file.read(),
            filetype="pdf"
        )

        extracted_text = ""

        for page in pdf_document:
            extracted_text += page.get_text()

        pdf_document.close()

        return extracted_text

    except Exception as error:
        return f"Error reading PDF: {error}"
