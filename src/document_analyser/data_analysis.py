import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from prompt.prompt_library import *

class DocumentAnalyser:
    """ Analyzes documents using a pre-trained model. Automatially logs all actions and supports session -based organization."""
    def __init__(self):
        try:
            self.loader= ModelLoader()
            self.llm=self.loader.load_llm

            # prepare parsers
            self.parser=JsonOutputParser(pydantic_object=Metadata) #pydantic model for structured output
            self.fixing_parser= OutputFixingParser.from_llm(llm=self.llm,parser=self.parser)

            self.prompt=prompt
            self.log.info("DocumentAnalyser initialized successfully.")

        except Exception as e:
            self.log.error("Error initializing DocumentAnalyser", error=str(e))
            raise DocumentPortalException("Error initializing DocumentAnalyser", sys)

    def analyze_document(self,document_text:str)->dict:
        """ Analyze a document's text and extract structured metadata & sunnary."""
        try:
            chain = self.prompt|self.llm|self.fixing_parser
            self.log.info("Meta-data analysis chain initialized successfully.")
            
            response =chain.invoke({
                "format_instructions":self.parser.get_format_instructions(),
                "document_text":document_text
            })

            self.log.info("Metadata extraction successful", keys=list(response.keys()))
            return response
        
        except Exception as e:
            self.log.error("Metadata extraction failed", error=str(e))
            raise DocumentPortalException("Metadata extraction failed") from e
        

