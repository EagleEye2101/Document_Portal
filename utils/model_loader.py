import os
import sys
from dotenv import load_dotenv
from utils.config_loader import load_config

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_groq import ChatGroq
#from langchain_openai import ChatOpenAI
from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

log = CustomLogger().get_logger(__name__)

class ModelLoader:
    """A Utility class to load embedding models and LLM models."""
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config = load_config()
        log.info("Configuration loaded successfully.",config_keys=list(self.config.keys()))
    
    
    def _validate_env(self):
        """ Validate necessary environment variables, Ensure API keys exists"""
        required_vars = ['GOOGLE_API_KEY','GROQ_API_KEY']
        self.api_keys={keys:os.getenv(keys) for keys in required_vars}
        missing = [k for k, v in self.api_keys.items() if not v ]
        if missing:
            log.error("Missing required environment variables", missing_vars=missing)
            raise DocumentPortalException(f"Missing required environment variables",sys)
        log.info("All required environment variables are set and validated.",available_vars=[k for k in self.api_keys if self.api_keys[k]])

            
    def load_embeddings(self):
        """ Load and return the embedding model based on configuration."""
        try:
            log.info("Loading embedding model...")
            model_name = self.config["embedding_model"]["model_name"]
            log.info("Loading embedding model", model_name=model_name)
            return GoogleGenerativeAIEmbeddings(
                model=model_name,
                api_key=self.api_keys['GOOGLE_API_KEY']
            )
        except Exception as e:
            log.error("Error loading embedding model", error=str(e))
            raise DocumentPortalException("Error loading embedding model", sys)
    
    
    def load_llm(self):
        """ Load and return the LLM model based on configuration."""
        """ Load LLM dynamicallu based on config """
        llm_block = self.config["llm"]
        log.info("Loading LLM model...")
        # Choose from Default provider or ENV variable
        provider_key = os.getenv("LLM_PROVIDER","google").lower() # Default to google if not set
        #provider_key = os.getenv("LLM_PROVIDER","groq").lower() # Default to google if not set

        if provider_key not in llm_block:
            log.error("LLM provider not found in config or configured", provider_key=provider_key)
            raise ValueError(f"Provider '{provider_key}' not found in config ")
        
        llm_config = llm_block[provider_key]
        provider=llm_config.get("provider").lower()
        model_name=llm_config.get("model_name")
        temperature=llm_config.get("temperature",0.2)
        max_tokens=llm_config.get("max_output_tokens",2048)

        log.info("LLM configuration. Loading LLM", provider=provider, model_name=model_name, temperature=temperature, max_tokens=max_tokens)
        if provider == "google":
            llm=ChatGoogleGenerativeAI(
                model=model_name,
                temperature=temperature,
                max_output_tokens=max_tokens,
                #api_key=self.api_keys['GOOGLE_API_KEY']
            )
            return llm
        elif provider == "groq":
            llm=ChatGroq(
                model=model_name,
                api_key=self.api_keys['GROQ_API_KEY'],
                temperature=temperature,
                #max_tokens=max_tokens    
            )
            return llm
        # elif provider == "openai":
        #     return ChatOpenAI(
        #         model_name=model_name,
        #         api_key=self.api_keys["OPENAI_API_KEY"],
        #         temperature=temperature,
        #         max_tokens=max_tokens
        #     )
        else:
            log.error("Unsupported LLM provider specified", provider=provider)
            raise ValueError(f"Unsupported LLM provider specified: {provider}") 
        
# Example usage
if __name__ == "__main__":
    loader = ModelLoader()

    # Test embedding model loading
    embeddings=loader.load_embeddings()
    log.info("Embedding model loaded successfully.", embedding_model=str(embeddings))
    # Test the embedding model with a sample text
    result = embeddings.embed_query("Hello, how are you?")
    print(f"Embedding result: {result}")
    log.info("embedding invocation result", result=result)
    

    # Test LLM model loading based on yaml config
    llm=loader.load_llm()
    log.info("LLM model loaded successfully.", llm_model=str(llm))

    # Test the ModelLoader with a simple prompt
    result = llm.invoke("Hello, how are you?")
    log.info("LLM invocation result", result=result)
