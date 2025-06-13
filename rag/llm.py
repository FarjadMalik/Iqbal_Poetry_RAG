"""LLM configuration for the RAG system."""

from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_community.llms import HuggingFacePipeline
from app.config import PERPLEXITY_API_KEY, LLM_MODEL

def initialize_llm():
    """Initialize and return the LLM."""
    # return ChatPerplexity(
    #     pplx_api_key=PERPLEXITY_API_KEY,
    #     model=LLM_MODEL,
    #     temperature=0.2,
    #     max_tokens=1024
    # )

    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        LLM_MODEL,
        trust_remote_code=True,
        device_map="auto",
        torch_dtype="auto"  # enables FP16 if available
    )

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        do_sample=True,
        max_new_tokens=1024,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.1,
        return_full_text=False
    )

    return HuggingFacePipeline(pipeline=pipe)


def get_rag_prompt():
    """Return the RAG prompt template."""
    # return ChatPromptTemplate.from_template(
    #     """You are an expert on Allama Iqbal's poetry based on the context. Use only the context to answer and cite his verses in the answer.
    #     Context: {context}
    #     Question: {question}
    #     Answer in structured Markdown:"""
    # )

    return PromptTemplate.from_template(
        """You are an expert on Allama Iqbal's poetry. Use the provided context to answer the question.        
        ### CONTEXT:{context}        
        ### QUESTION:{question}        
        ### ANSWER (Markdown formatted with poetic citations):
        """
    )

