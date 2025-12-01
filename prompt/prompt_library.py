from langchain_core.prompts import ChatPromptTemplate

#Prepare promot template
document_analysis_prompt=ChatPromptTemplate.from_template(""" 
You are a highly capable assisatnt trained to amalyze and summarize documents. 
Return ONLY valid JSON matching the exact schema below. 

{format_instructions}
                                        
Analyze this document:
{document_text}
""")

document_comparison_prompt=ChatPromptTemplate.from_template(""" an
You will be provided with content from two PDFs. Your task are as follows:
                                                            
1. Compare the content in two PDFs
2. Identify the differences in PDF and note down the page number
3. The output you provide must be page wise comparision content
4. If any page do not have any changes , mention "No Changes" for that page
                                                            
Input documents:                                       
{combined_docs}
Your response should follow this format :
{format_instructions}
""")

                                                            
PROMPT_REGISTRY={"document_analysis":document_analysis_prompt,"document_comparison":document_comparison_prompt}