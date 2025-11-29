"""
Document Processor Module
Handles loading and chunking company documents for the knowledge base.
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
import os

class DocumentProcessor:
    """Processes documents for the knowledge base"""
    
    def __init__(self, chunk_size=500, chunk_overlap=50):
        """
        Initialize the document processor.
        
        Args:
            chunk_size (int): Maximum size of each text chunk
            chunk_overlap (int): Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""],
            length_function=len
        )
    
    def load_documents(self, directory_path):
        """
        Load all documents from the specified directory.
        
        Args:
            directory_path (str): Path to directory containing documents
            
        Returns:
            list: List of loaded documents
            
        Raises:
            FileNotFoundError: If directory doesn't exist
        """
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        documents = []
        supported_extensions = {'.txt', '.pdf'}
        
        print(f"\n📂 Loading documents from: {directory_path}")
        
        for filename in sorted(os.listdir(directory_path)):
            file_path = os.path.join(directory_path, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Get file extension
            _, ext = os.path.splitext(filename)
            
            if ext not in supported_extensions:
                print(f"⏭️  Skipped: {filename} (unsupported format)")
                continue
            
            try:
                # Load based on file type
                if ext == '.txt':
                    loader = TextLoader(file_path, encoding='utf-8')
                elif ext == '.pdf':
                    loader = PyPDFLoader(file_path)
                
                loaded_docs = loader.load()
                documents.extend(loaded_docs)
                print(f"✅ Loaded: {filename} ({len(loaded_docs)} pages/sections)")
                
            except Exception as e:
                print(f"❌ Error loading {filename}: {str(e)}")
        
        print(f"\n📚 Total documents loaded: {len(documents)}")
        return documents
    
    def process_documents(self, documents):
        """
        Split documents into smaller chunks for better retrieval.
        
        Args:
            documents (list): List of documents to process
            
        Returns:
            list: List of document chunks
        """
        if not documents:
            print("⚠️  No documents to process")
            return []
        
        print(f"\n✂️  Splitting documents into chunks...")
        print(f"   Chunk size: {self.chunk_size} characters")
        print(f"   Chunk overlap: {self.chunk_overlap} characters")
        
        chunks = self.text_splitter.split_documents(documents)
        
        print(f"✅ Created {len(chunks)} chunks")
        
        return chunks
    
    def get_stats(self, chunks):
        """
        Get statistics about the processed chunks.
        
        Args:
            chunks (list): List of document chunks
            
        Returns:
            dict: Statistics about the chunks
        """
        if not chunks:
            return {"total_chunks": 0, "avg_chunk_size": 0, "sources": []}
        
        total_chars = sum(len(chunk.page_content) for chunk in chunks)
        avg_size = total_chars // len(chunks)
        sources = list(set(chunk.metadata.get('source', 'unknown') for chunk in chunks))
        
        return {
            "total_chunks": len(chunks),
            "avg_chunk_size": avg_size,
            "total_characters": total_chars,
            "sources": sources
        }


def main():
    """Test the document processor"""
    print("="*60)
    print("TESTING DOCUMENT PROCESSOR")
    print("="*60)
    
    # Initialize processor
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    
    # Load documents
    docs = processor.load_documents("data/documents")
    
    # Process into chunks
    chunks = processor.process_documents(docs)
    
    # Show statistics
    stats = processor.get_stats(chunks)
    print(f"\n📊 STATISTICS:")
    print(f"   Total chunks: {stats['total_chunks']}")
    print(f"   Average chunk size: {stats['avg_chunk_size']} characters")
    print(f"   Total characters: {stats['total_characters']}")
    print(f"   Source files: {len(stats['sources'])}")
    
    # Show sample chunk
    if chunks:
        print(f"\n📖 SAMPLE CHUNK:")
        print(f"{'='*60}")
        print(chunks[0].page_content)
        print(f"{'='*60}")
        print(f"Source: {chunks[0].metadata.get('source', 'unknown')}")


if __name__ == "__main__":
    main()