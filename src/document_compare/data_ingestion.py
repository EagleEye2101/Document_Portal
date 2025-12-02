import sys
from pathlib import path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocumentIngestion:
    def __init__(self,base_dir):
        self.log= CustomLogger().get_logger(__name__)
        self.base_dir=Path(base_dir)
        self.base_dir.mkdir(parents=True,exist_ok=True)
        self.log.info("DocumentIngestion initialized", base_directory=str(self.base_dir))

    def delete_existing_files(self):
        """ Delete existing uploaded files from the storage directory. """
        try:
            pass
        except Exception as e:
            self.log.error("Error deleting existing files", error=str(e))
            raise DocumentPortalException("Error deleting existing files", sys)
        
    def save_uploaded_files(self):
        """ Save newly uploaded files to the storage directory. """
        try:
            pass
        except Exception as e:
            self.log.error("Error saving uploaded files", error=str(e))
            raise DocumentPortalException("Error saving uploaded files", sys)
        
    def read_pdf(self,pdf_path: path) -> str:
        """ Read and extract text from PDF files. """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    self.log.error("PDF file is encrypted and cannot be read", pdf_path=pdf_path)
                    raise ValueError(f"PDF is encrypted:{pdf_path.name}")
                all_text = []
                for page_num in range(len(doc)):
                    page=doc.load_page(page_num)
                    text= page.get_text()
                    if text.strip():
                        all_text.append(f"/n--- Page {page_num + 1} ---/n{text}")
                self.log.info("PDF file read successfully", file=str(pdf_path),pages=len(all_text))
                return "\n".join(all_text)
        except Exception as e:
            self.log.error("Error reading PDF file", error=str(e))
            raise DocumentPortalException("Error reading PDF file", sys)