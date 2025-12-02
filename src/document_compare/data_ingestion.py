import sys
from pathlib import path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocumentIngestion:
    def __init__(self,base_dir:str="data/document_compare"):
        self.log= CustomLogger().get_logger(__name__)
        self.base_dir=Path(base_dir)
        self.base_dir.mkdir(parents=True,exist_ok=True)
        self.log.info("DocumentIngestion initialized", base_directory=str(self.base_dir))

    def delete_existing_files(self):
        """ Delete existing uploaded files from the storage directory. """
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.log.info("Deleted file", path=str(file))
                self.log.info("Existing files deleted successfully from storage directory.", directory=str(self.base_dir))
        except Exception as e:
            self.log.error("Error deleting existing files", error=str(e))
            raise DocumentPortalException("Error deleting existing files", sys)
        
    def save_uploaded_files(self,reference_file,actual_file):
        """ Save newly uploaded files to the storage directory. """
        try:
            self.delete_existing_files
            self.log.info("Uploaded files saved successfully.")

            ref_path=self.base_dir / reference_file.name
            act_path=self.base_dir / actual_file.name

            if not reference_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                self.log.error("Unsupported file format. Only PDF files are supported.", reference_file=reference_file.name, actual_file=actual_file.name)
                raise ValueError("Unsupported file format. Only PDF files are supported.")
            
            with open(ref_path,'wb') as f:
                f.write(reference_file.getbuffer())

            with open(act_path,'wb') as f:
                f.write(actual_file.getbuffer())

            self.log.info("Uploaded files saved successfully", reference=str(ref_path),actual=str(act_path))
            return ref_path, act_path
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
    
    def combine_documents(self)->str:
        try:
            content_dict={}
            doc_parts=[]

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix ==".pdf":
                    content_dict[filename.name]=self.read_pdf(filename)

            for filename, content in content_dict.items():
                doc_parts.append(f"Document:{filename}\n{content}")
            
            combined_text="\n\n".join(doc_parts)
            self.log.info("Document Combined",count=len(doc_parts))
            return combined_text
        
        except Exception as e:
            self.log.error(f"Error combining documents: {e}")
            raise DocumentPortalException("An error occurred while combining documents.",sys)
        
