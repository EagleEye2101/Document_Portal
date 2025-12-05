import sys
from dotenv import load_dotenv
import pandas as pd
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import SummaryResponse,PromptType
from prompt.prompt_library import PROMPT_REGISTRY
from utils.model_loader import ModelLoader
from langchain_core.output_parsers import JsonOutputParser
#from langchain_core.output_parsers import OutputFixingParser
#from langchain.output_parsers import OutputFixingParser
try:
    from langchain.output_parsers import OutputFixingParser
except Exception:
    try:
        from langchain_core.output_parsers import OutputFixingParser
    except Exception:
        OutputFixingParser = None

try:
    from langchain_core.output_parsers import JsonOutputParser
except Exception:
    try:
        from langchain.output_parsers import JsonOutputParser
    except Exception:
        JsonOutputParser = None

class DocumentComparatorLLM:
    def __init__(self):
        load_dotenv()
        self.log= CustomLogger().get_logger(__name__)
        self.loader= ModelLoader()
        self.llm= self.loader.load_llm()
        #self.parser= JsonOutputParser(pydantic_object=SummaryResponse)
        # prepare parsers (ensure parser classes are available)
        if JsonOutputParser is None:
            self.log.error("JsonOutputParser not available in installed LangChain packages")
            raise DocumentPortalException("JsonOutputParser not found. Install a compatible langchain/langchain-core package.", sys)

        self.parser = JsonOutputParser(pydantic_object=SummaryResponse)  # pydantic model for structured output
        # If OutputFixingParser is available, initialize it; otherwise keep None and
        # use a fallback parsing flow during analysis.
        #self.fixing_parser= OutputFixingParser.from_llm(parser=self.parser,llm=self.llm)
        if OutputFixingParser is not None:
            self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser,llm=self.llm)
        else:
            self.fixing_parser = None
        self.prompt= PROMPT_REGISTRY[PromptType.DOCUMENT_COMPARISON.value]
        self.chain=self.prompt|self.llm|self.parser
        self.log.info("DocumentComparatorLLM initialized successfully.",model=self.llm)

    def compare_documents(self,combined_docs: str)-> pd.DataFrame:
        """ Compare two documents and return the differences. """
        try:
            inputs = {
                "combined_docs": combined_docs,
                "format_instructions": self.parser.get_format_instructions() 
            }
            self.log.info("Invoking  document comparison LLM Chain", inputs= inputs)
            response=self.chain.invoke(inputs)
            self.log.info("Chain invoked successfully. Document comparison completed successfully.",response_preview=str(response)[:200])
            return self._format_response(response)
        
        except Exception as e:
            self.log.error("Error comparing documents", error=str(e))
            raise DocumentPortalException("Error comparing documents", sys) 
        
    def _format_response(self,response_parsed: list[dict]) -> pd.DataFrame:

        """ Format the LLM response into structured data. """
        try:
            df=pd.DataFrame(response_parsed)
            self.log.info("Formatted response into DataFrame successfully.", dataframe=df)
            return df
        except Exception as e:
            self.log.error("Error formatting response", error=str(e))
            raise DocumentPortalException("Error formatting response", sys) 