from pydantic import BaseModel, Field
from typing import List, Optional,Dict,Any,Union

#pydantic model added for validation and structure

class Metadata(BaseModel):
    Sunnary: List[str] = Field(default_factory=list, description="List of summary points extracted from the document")
    Title:str
    Author:str
    DateCreated:str
    LastModifiedDate:str
    Publisher:str
    Language:str
    PageCount:Union[int,str]
    SentimentTone:str
