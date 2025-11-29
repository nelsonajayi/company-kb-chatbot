"""
Vector Store Module
Manages document embeddings and retrieval using ChromaDB.
"""

import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Any

class VectorStore:
    """Vector database for storing and retrieving document embeddings"""
    
    def __init__(self, collection_name="company_docs", persist_directory="./data/chroma_db"):
        """
        Initialize the vector store.
        
        Args:
            collection_name (str): Name of the document collection
            persist_directory (str): Directory to persist the database
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        print(f"✅ Vector store initialized")
        print(f"   Collection: {collection_name}")
        print(f"   Location: {persist_directory}")
        print(f"   Documents in store: {self.collection.count()}")
    
    def add_documents(self, chunks: List[Any]) -> None:
        """
        Add document chunks to the vector store.
        
        Args:
            chunks: List of document chunks with content and metadata
        """
        if not chunks:
            print("⚠️  No chunks to add")
            return
        
        print(f"\n📥 Adding {len(chunks)} chunks to vector store...")
        
        # Prepare data
        documents = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        ids = [f"doc_{i}" for i in range(len(chunks))]
        
        # Add to ChromaDB in batches to avoid memory issues
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            end_idx = min(i + batch_size, len(documents))
            
            self.collection.add(
                documents=documents[i:end_idx],
                metadatas=metadatas[i:end_idx],
                ids=ids[i:end_idx]
            )
            
            print(f"   Processed {end_idx}/{len(documents)} chunks")
        
        print(f"✅ Successfully added {len(chunks)} chunks")
        print(f"📊 Total documents in store: {self.collection.count()}")
    
    def search(self, query: str, n_results: int = 3) -> Dict[str, Any]:
        """
        Search for relevant documents.
        
        Args:
            query (str): Search query
            n_results (int): Number of results to return
            
        Returns:
            dict: Search results with documents, metadata, and distances
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=min(n_results, self.collection.count())
        )
        
        return results
    
    def get_count(self) -> int:
        """
        Get the total number of documents in the store.
        
        Returns:
            int: Number of documents
        """
        return self.collection.count()
    
    def clear(self) -> None:
        """Clear all documents from the collection"""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print("🗑️  Vector store cleared")
    
    def delete_collection(self) -> None:
        """Permanently delete the collection"""
        self.client.delete_collection(self.collection_name)
        print(f"🗑️  Collection '{self.collection_name}' deleted")


def main():
    """Test the vector store"""
    from document_processor import DocumentProcessor
    
    print("="*60)
    print("TESTING VECTOR STORE")
    print("="*60)
    
    # Load and process documents
    processor = DocumentProcessor()
    docs = processor.load_documents("data/documents")
    chunks = processor.process_documents(docs)
    
    # Initialize vector store
    vector_store = VectorStore()
    
    # Clear existing data for clean test
    if vector_store.get_count() > 0:
        print("\n🗑️  Clearing existing data...")
        vector_store.clear()
    
    # Add documents
    vector_store.add_documents(chunks)
    
    # Test search
    print("\n" + "="*60)
    print("TESTING SEARCH")
    print("="*60)
    
    test_queries = [
        "What is the vacation policy?",
        "Can I work from home?",
        "How do I submit expenses?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-"*60)
        
        results = vector_store.search(query, n_results=2)
        
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            print(f"\nResult {i+1} (relevance: {1-distance:.2%}):")
            print(f"Source: {metadata.get('source', 'Unknown')}")
            print(f"Content preview: {doc[:200]}...")


if __name__ == "__main__":
    main()