"""Main RAG system implementation."""


from rag.vector_store import initialize_vector_store, build_vector_store_from_json
from rag.retriever import configure_retriever
from rag.llm import initialize_llm, get_rag_prompt
# from utils.feedback_logger import FeedbackLogger
from utils.error_handling import handle_rag_error
from app.config import SCORE_THRESHOLD, JSON_FILE_PATH

class IqbalRAGSystem:
    """Manages the RAG system for Iqbal's poetry."""

    def __init__(self):
        """Initialize the RAG system components."""
        # Build or load vector store
        self.vector_store = build_vector_store_from_json(JSON_FILE_PATH)
        self.retriever = configure_retriever(self.vector_store)
        self.llm = initialize_llm()
        self.prompt = get_rag_prompt()
        self.chain = self.prompt | self.llm
        # self.feedback_logger = FeedbackLogger()

    @handle_rag_error
    def query_rag(self, question):
        """Process a query through the RAG system."""
        print(f"**********************************************************************")
        print(f"query_rag: {question}")
        docs = self.retriever.invoke(question, config={'score_threshold': SCORE_THRESHOLD})
        if not docs:
            return "No relevant poems found", []

        print(f"docs: {docs}")
        context = "\n\n".join(doc.page_content for doc in docs)
        print(f"context: {context}")
        context_ids = [doc.metadata.get("poem_id", "") for doc in docs]
        print(f"context_ids: {context_ids}")
        
        response = self.chain.invoke({
            'context': context,
            'question': question
        })
        print(f"response: {response}")
        print(f"**********************************************************************")
        
        return response, context_ids

    # def log_feedback(self, query, response, feedback, comment, context_ids):
    #     """Log user feedback."""
    #     self.feedback_logger.log_feedback(query, response, feedback, comment, context_ids)
