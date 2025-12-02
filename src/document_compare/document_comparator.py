import sys
from dotenv import load_dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
from prompt.prompt_library import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
#from langchain_core.output_parsers import OutputFixingParser
from langchain.output_parsers import OutputFixingParser

class DocumentComparatorLLM:
    def __init__(self):
        load_dotenv()
        self.log= CustomLogger().get_logger(__file__)
        self.loader= ModelLoader()
        self.llm= self.loader.load_llm()
        self.parser= JsonOutputParser(pydantic_object=SummaryResponse)
        self.fixing_parser= OutputFixingParser.from_llm(parser=self.parser,llm=self.llm)
        self.prompt= PROMPT_REGISTRY["document_comparison"]
        self.chain=self.prompt|self.llm|self.parser|self.fixing_parser
        self.log.info("DocumentComparatorLLM initialized successfully.")
    def compare_documents(self,combined_docs: str)-> pd.DataFrame:
        """ Compare two documents and return the differences. """
        try:
            inputs = {
                "combined_docs": combined_docs,
                "format_instructions": self.parser.get_format_instructions() 
            }
            self.log.info("Starting document comparison", inputs= inputs)
            response=self.chain.invoke(inputs)
            self.log.info("Document comparison completed successfully.",response=response)

            return self._format_response(response)
        
        except Exception as e:
            self.log.error("Error comparing documents", error=str(e))
            raise DocumentPortalException("Error comparing documents", sys) 
        
    def _format_response(self,response_parsed: dict) -> pd.DataFrame:

        """ Format the LLM response into structured data. """
        try:
            df=pd.DataFrame(response_parsed)
            self.log.info("Formatted response into DataFrame successfully.", dataframe=df)
            return df
        except Exception as e:
            self.log.error("Error formatting response", error=str(e))
            raise DocumentPortalException("Error formatting response", sys) 