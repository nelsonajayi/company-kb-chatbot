"""
Document Indexing Script
Processes and indexes all company documents into the vector store.
Run this script whenever you add new documents.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from document_processor import DocumentProcessor
from vector_store import VectorStore


def index_documents(documents_path="data/documents", force_reindex=False):
    """
    Index all documents in the specified directory.
    
    Args:
        documents_path (str): Path to documents directory
        force_reindex (bool): If True, clear existing index before adding
    """
    print("="*70)
    print(" "*20 + "DOCUMENT INDEXING")
    print("="*70)
    
    # Initialize components
    print("\n📋 Step 1: Initializing components...")
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    vector_store = VectorStore()
    
    # Check if we should reindex
    existing_count = vector_store.get_count()
    if existing_count > 0:
        if force_reindex:
            print(f"\n⚠️  Found {existing_count} existing documents. Clearing for reindex...")
            vector_store.clear()
        else:
            print(f"\n⚠️  Found {existing_count} existing documents.")
            response = input("   Clear and reindex? (y/n): ").lower()
            if response == 'y':
                vector_store.clear()
            else:
                print("   Keeping existing documents. New documents will be added.")
    
    # Load documents
    print("\n📋 Step 2: Loading documents...")
    try:
        docs = processor.load_documents(documents_path)
        
        if not docs:
            print("❌ No documents found. Please add documents to the 'data/documents' folder.")
            return False
            
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return False
    
    # Process documents
    print("\n📋 Step 3: Processing documents into chunks...")
    chunks = processor.process_documents(docs)
    
    if not chunks:
        print("❌ No chunks created. Check your documents.")
        return False
    
    # Show statistics
    stats = processor.get_stats(chunks)
    print(f"\n📊 Processing Statistics:")
    print(f"   • Total chunks: {stats['total_chunks']}")
    print(f"   • Average chunk size: {stats['avg_chunk_size']} characters")
    print(f"   • Source files: {len(stats['sources'])}")
    
    # Index documents
    print("\n📋 Step 4: Indexing into vector store...")
    vector_store.add_documents(chunks)
    
    # Verify
    print("\n📋 Step 5: Verifying index...")
    final_count = vector_store.get_count()
    print(f"✅ Indexing complete! Total documents in store: {final_count}")
    
    # Test search
    print("\n📋 Step 6: Testing search...")
    test_query = "vacation policy"
    results = vector_store.search(test_query, n_results=1)
    if results['documents'][0]:
        print(f"✅ Search test passed (query: '{test_query}')")
    else:
        print(f"⚠️  Search test returned no results")
    
    print("\n" + "="*70)
    print("✨ INDEXING COMPLETE - Your knowledge base is ready!")
    print("="*70)
    
    return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Index company documents')
    parser.add_argument('--path', default='data/documents', 
                       help='Path to documents directory')
    parser.add_argument('--force', action='store_true',
                       help='Force reindex (clear existing data)')
    
    args = parser.parse_args()
    
    success = index_documents(args.path, args.force)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()