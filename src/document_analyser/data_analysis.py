import os
import sys
from utils.model_loader import ModelLoader
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException
from model.models import *
# Support multiple langchain versions: try both locations for the parsers
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

from prompt.prompt_library import *

class DocumentAnalyser:
    """ Analyzes documents using a pre-trained model. Automatially logs all actions and supports session -based organization."""
    def __init__(self):
        try:
            self.loader= ModelLoader()
            self.log = CustomLogger().get_logger(__file__)
            # load the LLM instance (call the loader method)
            self.llm = self.loader.load_llm()

            # prepare parsers (ensure parser classes are available)
            if JsonOutputParser is None:
                self.log.error("JsonOutputParser not available in installed LangChain packages")
                raise DocumentPortalException("JsonOutputParser not found. Install a compatible langchain/langchain-core package.", sys)

            self.parser = JsonOutputParser(pydantic_object=Metadata)  # pydantic model for structured output

            # If OutputFixingParser is available, initialize it; otherwise keep None and
            # use a fallback parsing flow during analysis.
            if OutputFixingParser is not None:
                self.fixing_parser = OutputFixingParser.from_llm(llm=self.llm, parser=self.parser)
            else:
                self.fixing_parser = None

            self.prompt=prompt
            self.log.info("DocumentAnalyser initialized successfully.")

        except Exception as e:
            self.log.error("Error initializing DocumentAnalyser", error=str(e))
            raise DocumentPortalException("Error initializing DocumentAnalyser", sys)

    def analyze_document(self,document_text:str)->dict:
        """ Analyze a document's text and extract structured metadata & sunnary."""
        try:
            # If we have the runnable OutputFixingParser available, use the original chain
            if self.fixing_parser is not None:
                chain = self.prompt | self.llm | self.fixing_parser
                self.log.info("Meta-data analysis chain initialized successfully.")
                response = chain.invoke({
                    "format_instructions": self.parser.get_format_instructions(),
                    "document_text": document_text,
                })
            else:
                # Fallback: construct a prompt manually, call the LLM, then parse
                self.log.info("OutputFixingParser unavailable; using fallback LLM+Json parser flow.")
                format_instructions = self.parser.get_format_instructions()
                prompt_text = (
                    "You are a highly capable assistant trained to analyze and summarize documents.\n"
                    "Return ONLY valid JSON matching the exact schema below.\n\n"
                    f"{format_instructions}\n\n"
                    "Analyze this document:\n"
                    f"{document_text}\n"
                )
                completion = self.llm.invoke(prompt_text)
                # extract text from completion object if needed
                if isinstance(completion, str):
                    completion_text = completion
                else:
                    completion_text = getattr(completion, 'text', None) or getattr(completion, 'content', None) or str(completion)

                response = self.parser.parse(completion_text)

            self.log.info("Metadata extraction successful", keys=list(response.keys()))
            return response
        
        except Exception as e:
            self.log.error("Metadata extraction failed", error=str(e))
            raise DocumentPortalException("Metadata extraction failed", sys) from e
        

