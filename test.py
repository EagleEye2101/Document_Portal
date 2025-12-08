#-------- Test code for document ingestion and analysis using a PDFHandler and DocumentAnalyzer
# import os
# from pathlib import Path
# from src.document_analyser.data_ingestion import DocumentHandler 
# from src.document_analyser.data_analysis import DocumentAnalyser

# #Path to the PDF you want to test 
# PDF_PATH=r"/Users/kiran_mac/Documents/AI_Training/GenAI_KrishNaik/Document_Portal/data/document_analysis/sample.pdf"

# #Dummy file wrapper to simulate uploaded file(Stramlit style)

# class DummyFile:
#     def __init__(self,file_path):
#         self.name=Path(file_path).name
#         self._file_path = file_path
#     def getbuffer(self):
#         return open(self._file_path,"rb").read()


# def main():
#     try:
#         # ---------- STEP 1 : Data Ingestion ----------
#         print("----- STEP 1: Data Ingestion - Starting PDF ingestion...-----")
#         dummy_pdf = DummyFile(PDF_PATH)

#         handler=DocumentHandler(session_id="test_ingestion_analysis")
#         saved_path=handler.save_pdf(dummy_pdf)
#         print(f"PDF saved at: {saved_path}")

#         test_content = handler.read_pdf(saved_path)
#         print(f"Extracted test length :{len(test_content)} characters\n")

#         # ---------- STEP 2 : Data Analysis ----------
#         print("----- STEP 2: Data Analysis - Starting metadata analysis...-----")
#         analyzer= DocumentAnalyser()
#         analysis_result = analyzer.analyze_document(test_content)

#         #---------- STEP 3 : Display Results ----------
#         print("----- STEP 3: Analysis Results \n==== METADATA ANALYSIS RESULT === -----")
#         for key, value in analysis_result.items():
#             print(f"{key}: {value}\n")
      
#     except Exception as e:
#         print(f"Error during testing : {e}")

# if __name__ == "__main__":
#     main()

# # --------Testing document_comparator.py using LLM --------
# import io
# from pathlib import Path
# from src.document_compare.data_ingestion import DocumentIngestion
# from src.document_compare.document_comparator import DocumentComparatorLLM

# # ---- Setup : Load local PDF files uf thet were uploaded-------#
# def load_fake_uploaded_file(file_path:Path):
#     """ Simulate an uploaded file by reading from disk. """
#     return io.BytesIO(file_path.read_bytes())
# # ---- Step 1 : Save and combine PDFs -------#
# def test_compare_documents():
#     ref_path= Path("/Users/kiran_mac/Documents/AI_Training/GenAI_KrishNaik/Document_Portal/data/document_compare/DukeSepBill.pdf")
#     act_path= Path("/Users/kiran_mac/Documents/AI_Training/GenAI_KrishNaik/Document_Portal/data/document_compare/DukeDecBill.pdf")
#     # Wrap them like Streamlit UploadedFile style 
#     class FakeUpload:
#         def __init__(self, file_path:Path):
#             self.name=file_path.name
#             self._buffer=file_path.read_bytes()

#         def getbuffer(self):
#             return self._buffer
#     # Instantiate     
#     comparator= DocumentIngestion()
#     ref_upload = FakeUpload(ref_path)
#     act_upload = FakeUpload(act_path)
#     # save files and combine
#     ref_file,act_file = comparator.save_uploaded_files(ref_upload,act_upload)
#     combined_text = comparator.combine_documents() 
#     # delete old session folders
#     comparator.clean_old_sessions(keep_latest=10)

#     print ("\n Combined Text Preview (first 1000 chars):\n ")
#     print(combined_text[:1000])
#     # ---- Step 2 : Run LLM Comparison -----#
#     llm_comparator = DocumentComparatorLLM()
#     comparison_df=llm_comparator.compare_documents(combined_text)

#     print("\n ==== COMPARISON RESULT =====")
#     print(comparison_df.head())

# # --- test the code --- # 
# if __name__ == "__main__":
#     test_compare_documents()

# # -------------------testing single_document_chat-------------------#


# import sys
# from pathlib import Path 
# from langchain_community.vectorstores import FAISS
# from src.single_document_chat.data_ingestion import SingleDocIngestor
# from src.single_document_chat.retrieval import ConversationalRAG 
# from utils.model_loader import ModelLoader

# FAISS_INDEX_PATH= Path("faiss_index")

# def test_conversational_rag_on_pdf(pdf_path:str,question:str):
#     try:
#         model_loader=ModelLoader()
#         if FAISS_INDEX_PATH.exists():
#             print("Loading existing FAISS index....")
#             embeddings=model_loader.load_embeddings()
#             vectorstore=FAISS.load_local(folder_path=str(FAISS_INDEX_PATH),embeddings=embeddings,allow_dangerous_deserialization=True)
#             retriever=vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":5})
#         else:
#             # Step 2: Ingest document and create retriever
#             print("FAISS index not found. Ingestion PDF and creating index...")
#             with open(pdf_path,"rb") as f:
#                 uploaded_files=[f]
#                 ingestor=SingleDocIngestor()
#                 retriever=ingestor.ingest_files(uploaded_files)
#         print("Running Conversational RAG...")
#         session_id="test_conversational_rag"
#         rag=ConversationalRAG(retriever=retriever,session_id=session_id)

#         response=rag.invoke(question)
#         print(f"\n Question: {question}\n Answer:{response}")

#     except Exception as e:
#         print(f"Test Failed: {str(e)}")
#         sys.exit(1)
# if __name__=="__main__":
#     #Example PDF path and question
#     pdf_path=r"/Users/kiran_mac/Documents/AI_Training/GenAI_KrishNaik/Document_Portal/data/single_document_chat/DukeDecBill.pdf"
#     question="what is the main topic of the document?"

#     if not Path(pdf_path).exists():
#         print(f"PDF files does not exists at : {pdf_path}")
#         sys.exit(1)

#     # Run the test 
#     test_conversational_rag_on_pdf(pdf_path,question)


## Testing multi document chat 
import sys
from pathlib import Path
from archive.src.multi_document_chat.data_ingestion import DocumentIngestor
from archive.src.multi_document_chat.retrieval import ConversationalRAG
def test_document_ingestion_and_rag():
    try:
        test_files=[
            #"data/multi_document_chat/NIPS-2017-attention-is-all-you-need-Paper.pdf",
            "data/multi_document_chat/DukeDecBill.pdf",
            "data/multi_document_chat/Copy of Jeev Ajeev Session 2 guide .docx"
           # "data/multi_document_chat/mycontacts.txt"
        ]
        uploaded_files=[]
        for file_path in test_files:
            if Path(file_path).exists():
                uploaded_files.append(open(file_path,"rb"))
            else:
                print(f"Files does not exist:{file_path}")
        if not uploaded_files:
            print("No valid file to upload ")
            sys.exit(1)

        # Step 2 : Ingest document and create retriever 
                
        ingestor=DocumentIngestor()
        retriever = ingestor.ingest_files(uploaded_files)

        for f in uploaded_files:
            f.close()
        
        print ("Running conversactional RAG...")
        session_id="test_multi_doc_ingestion_and_rag"
        
        rag=ConversationalRAG(retriever=retriever,session_id=session_id)
        question="What are the key findings in the DukeDecBill file"
        response=rag.invoke(question)
        print(f"\nQuestion:{question}\nAnswer:{response}")

    except Exception as e:
        print (f"Test failed:{str(e)}")
        sys.exit(1)

if __name__=="__main__":
    # Run the test 
    test_document_ingestion_and_rag()

