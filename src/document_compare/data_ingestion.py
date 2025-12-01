import sys
from pathlib import path
import fitz
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException


class DocumentComparator:
    def __init__(self):
        pass
    def delete_existing_files(self):
        """ Delete existing uploaded files from the storage directory. """
        pass
    def save_uploaded_files(self):
        """ Save newly uploaded files to the storage directory. """
        pass
    def read_pdf(self):
        """ Read and extract text from PDF files. """
        pass