from PyPDF2 import PdfReader
from langchain_core.documents import Document


def extract_documents_from_pdf(file_path: str):
    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text and page_text.strip():
            document = Document(
                page_content=page_text,
                metadata={
                    "page": page_number,
                    "source": file_path
                }
            )

            documents.append(document)

    return documents