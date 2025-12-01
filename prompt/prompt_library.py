from langchain_core.prompts import ChatPromptTemplate

#Prepare promot template
prompt=ChatPromptTemplate.from_template(""" 
You are a highly capable assisatnt trained to amalyze and summarize documents. 
Return ONLY valid JSON matching the exact schema below. 

{format_instructions}
                                        
Analyze this document:
{document_text}
""")