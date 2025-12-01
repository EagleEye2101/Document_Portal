import os
from pathlib import Path
from src.document_analyser.data_ingestion import DocumentHandler 
from src.document_analyser.data_analysis import DocumentAnalyser

#Path to the PDF you want to test 
PDF_PATH=r"/Users/kiran_mac/Documents/AI_Training/GenAI_KrishNaik/Document_Portal/data/document_analysis/sample.pdf"

#Dummy file wrapper to simulate uploaded file(Stramlit style)

class DummyFile:
    def __init__(self,file_path):
        self.name=Path(file_path).name
        self._file_path = file_path
    def getbuffer(self):
        return open(self._file_path,"rb").read()


def main():
    try:
        # ---------- STEP 1 : Data Ingestion ----------
        print("----- STEP 1: Data Ingestion - Starting PDF ingestion...-----")
        dummy_pdf = DummyFile(PDF_PATH)

        handler=DocumentHandler(session_id="test_ingestion_analysis")
        saved_path=handler.save_pdf(dummy_pdf)
        print(f"PDF saved at: {saved_path}")

        test_content = handler.read_pdf(saved_path)
        print(f"Extracted test length :{len(test_content)} characters\n")

        # ---------- STEP 2 : Data Analysis ----------
        print("----- STEP 2: Data Analysis - Starting metadata analysis...-----")
        analyzer= DocumentAnalyser()
        analysis_result = analyzer.analyze_document(test_content)

        #---------- STEP 3 : Display Results ----------
        print("----- STEP 3: Analysis Results \n==== METADATA ANALYSIS RESULT === -----")
        for key, value in analysis_result.items():
            print(f"{key}: {value}\n")
      
    except Exception as e:
        print(f"Error during testing : {e}")

if __name__ == "__main__":
    main()