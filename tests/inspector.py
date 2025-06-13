import os
import json
from langchain_chroma import Chroma
from langchain_core.documents import Document
from pprint import pprint
import pandas as pd

class ChromaVectorStoreInspector:
    def __init__(self, persist_dir, embeddings):
        """
        Initialize inspector with existing Chroma store
        
        Args:
            persist_dir (str): Directory where Chroma data is stored
            embeddings: Embeddings model used in the original store
        """
        self.vector_store = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )
        self.collection = self.vector_store._collection

    def get_store_metadata(self):
        """Get critical metadata about the vector store"""
        return {
            "document_count": self._get_document_count(),
            "embedding_function": str(self.vector_store._embedding_function),
            "persist_directory": self.vector_store._persist_directory,
            "collection_name": self.collection.name
        }

    def _get_document_count(self):
        """Get total number of documents in the collection"""
        return self.collection.count()

    def sample_documents(self, n=5):
        """Retrieve sample documents with metadata"""
        results = self.collection.get(limit=n)
        return [
            {
                "id": doc_id,
                "metadata": meta,
                "content": doc[:200] + "..." if len(doc) > 200 else doc
            }
            for doc_id, meta, doc in zip(
                results["ids"],
                results["metadatas"],
                results["documents"]
            )
        ]

    def analyze_metadata(self):
        """Analyze metadata distribution patterns"""
        results = self.collection.get()
        print(results)
        # df = pd.DataFrame(results["metadatas"])
        
        # analysis = {}
        # if not df.empty:
        #     analysis["metadata_fields"] = list(df.columns)
        #     analysis["book_title_distribution"] = df["book_title"].value_counts().to_dict()
        #     analysis["missing_values"] = df.isna().sum().to_dict()
        
        # return analysis

    def test_semantic_search(self, query, k=3):
        """Test the vector search functionality"""
        results = self.vector_store.similarity_search(query, k=k)
        return [
            {
                "content": doc.page_content[:150] + "...",
                "metadata": doc.metadata,
                "score": doc.metadata.get("score", 0.0)
            }
            for doc in results
        ]

    def full_health_check(self):
        """Comprehensive store verification report"""
        return {
            "metadata": self.get_store_metadata(),
            "sample_documents": self.sample_documents(),
            "metadata_analysis": self.analyze_metadata(),
            "search_test": self.test_semantic_search("philosophical concepts")
        }

    def verify_against_source(self, json_path):
        """Verify vector store contents against source JSON"""
        with open(json_path, "r") as f:
            source_data = json.load(f)
        
        source_ids = {p["poem_id"] for p in source_data}
        stored_ids = set(self.collection.get()["ids"])
        
        return {
            "source_count": len(source_ids),
            "stored_count": len(stored_ids),
            "missing_in_store": source_ids - stored_ids,
            "extra_in_store": stored_ids - source_ids
        }

# Usage example
if __name__ == "__main__":
    from rag.embeddings import get_embeddings  # Your existing embeddings setup
    from app.config import CHROMA_DB_DIR  # Your config
    
    # Initialize inspector
    inspector = ChromaVectorStoreInspector(
        persist_dir=CHROMA_DB_DIR,
        embeddings=get_embeddings()
    )
    
    # print("\n=== Vector Store Metadata ===")
    # pprint(inspector.get_store_metadata())
    
    # print("\n=== Document Samples ===")
    # pprint(inspector.sample_documents())
    
    # print("\n=== Metadata Analysis ===")
    # pprint(inspector.analyze_metadata())
    
    # print("\n=== Source Verification ===")
    # verification = inspector.verify_against_source("data/processed_data/iqbal_poems_rag.json")
    # pprint(verification)
    
    # print("\n=== Search Test Results ===")
    # pprint(inspector.test_semantic_search("lost"))

    print("\n=== Full Health Check ===")
    pprint(inspector.full_health_check())
