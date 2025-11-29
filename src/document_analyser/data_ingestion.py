import os
import fitz  # PyMuPDF
import uuid
from datetime import datetime
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

class DocumentHandler:
    """ Haandle PDF saving and reading operations. Automatically log all actions and suports session-based organization. """
    def __init__(self,data_dir=None,session_id=None):
        try:
            self.log=CustomLogger().get_logger(__name__)
            self.data_dir = data_dir or os.getenv(
                "DATA_STORAGE_PATH",
                os.path.join(os.getcwd(), "data", "document_analysis")
                )
            self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"

            # Create base session directory if it doesn't exist
            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)
            self.log.info("PDFHandler initialized", session_id=self.session_id, session_path=self.session_path)
        except Exception as e:
            self.log.error("Error initializing DocumentHandler", error=str(e))
            raise DocumentPortalException("Error initializing DocumentHandler", e) from e


    def save_pdf(self):
        try:
            pass
        except Exception as e:
            self.log.error("Error saving PDF", error=str(e))
            raise DocumentPortalException("Error saving PDF", e) from e
    def read_pdf(self):
        try:
            pass
        except Exception as e:
            self.log.error("Error reading PDF", error=str(e))
            raise DocumentPortalException("Error reading PDF", e) from e
        
#test the code 
if __name__ == "__main__":
    handler = DocumentHandler()
   # handler.save_pdf()
   # handler.read_pdf()
    print(f"Session ID: {handler.session_id}")
    print(f"Session Path: {handler.session_path}")
