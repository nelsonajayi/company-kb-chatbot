"""
Chatbot Module
RAG-based chatbot using Ollama and ChromaDB for company knowledge base.
"""

import subprocess
import json
from typing import Dict, List, Any
from vector_store import VectorStore


class CompanyKBChatbot:
    """Company Knowledge Base Chatbot using RAG"""
    
    def __init__(self, model="llama2"):
        """
        Initialize the chatbot.
        
        Args:
            model (str): Ollama model to use (llama2, mistral, llama3, etc.)
        """
        self.model = model
        self.vector_store = VectorStore()
        self.conversation_history = []
        
        # Verify Ollama is available
        if not self._check_ollama():
            raise RuntimeError(
                "Ollama is not available. Please ensure:\n"
                "1. Ollama is installed from https://ollama.ai\n"
                "2. You've activated the conda environment: conda activate company-kb\n"
                "3. Test with: ollama --version"
            )
        
        print(f"🤖 Chatbot initialized")
        print(f"   Model: {model}")
        print(f"   Knowledge base size: {self.vector_store.get_count()} documents")
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is installed and accessible"""
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def search_knowledge_base(self, query: str, n_results: int = 3) -> Dict[str, Any]:
        """
        Search the knowledge base for relevant documents.
        
        Args:
            query (str): User's question
            n_results (int): Number of documents to retrieve
            
        Returns:
            dict: Search results
        """
        return self.vector_store.search(query, n_results)
    
    def format_context(self, search_results: Dict[str, Any]) -> tuple:
        """
        Format search results into a context string.
        
        Args:
            search_results (dict): Results from vector store search
            
        Returns:
            tuple: (formatted_context_string, list_of_sources)
        """
        context_parts = []
        sources = []
        
        for i, (doc, metadata) in enumerate(zip(
            search_results['documents'][0],
            search_results['metadatas'][0]
        )):
            source = metadata.get('source', 'Unknown')
            # Extract just the filename (works for both / and \ paths)
            source_name = source.split('/')[-1].split('\\')[-1] if ('/' in source or '\\' in source) else source
            
            context_parts.append(
                f"[Document {i+1} - {source_name}]:\n{doc}"
            )
            sources.append(source_name)
        
        context = "\n\n".join(context_parts)
        # Remove duplicates while preserving order
        unique_sources = list(dict.fromkeys(sources))
        
        return context, unique_sources
    
    def generate_response(self, user_question: str, context: str) -> str:
        """Generate a response using Ollama."""
        
        system_prompt = "You are a helpful AI assistant for ACME Corporation. Answer questions based ONLY on the provided documents. Be professional and concise."
        
        prompt = f"{system_prompt}\n\nContext:\n{context}\n\nQuestion: {user_question}\n\nAnswer:"

        try:
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                timeout=120
            )
            
            if result.returncode != 0:
                return f"Error generating response: {result.stderr}"
            
            response = result.stdout.strip()
            response = response.replace('/bye', '').strip()
            
            if not response:
                return "No response generated. Please try again."
            
            return response
            
        except subprocess.TimeoutExpired:
            return "Response timed out after 2 minutes. Please try a simpler question."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat(self, user_question: str) -> Dict[str, Any]:
        """
        Main chat interface - orchestrates the full RAG pipeline.
        
        Args:
            user_question (str): The user's question
            
        Returns:
            dict: Response containing answer and sources
        """
        # 1. Search knowledge base
        search_results = self.search_knowledge_base(user_question, n_results=3)
        
        # Check if we found relevant documents
        if not search_results['documents'][0]:
            return {
                "answer": "I couldn't find any relevant information in the company documents.",
                "sources": []
            }
        
        # 2. Format context
        context, sources = self.format_context(search_results)
        
        # 3. Generate response
        answer = self.generate_response(user_question, context)
        
        # 4. Store in conversation history
        self.conversation_history.append({
            "question": user_question,
            "answer": answer,
            "sources": sources
        })
        
        return {
            "answer": answer,
            "sources": sources
        }
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the full conversation history"""
        return self.conversation_history
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []


def main():
    """Test the chatbot"""
    print("="*70)
    print(" "*25 + "CHATBOT TEST")
    print("="*70)
    
    try:
        chatbot = CompanyKBChatbot(model="llama2")
        
        test_questions = [
            "How many vacation days do I get after 3 years?",
            "Can I work from home?",
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n{'='*70}")
            print(f"Test {i}/{len(test_questions)}")
            print(f"{'='*70}")
            print(f"Question: {question}")
            print("-"*70)
            
            response = chatbot.chat(question)
            
            print(f"\nAnswer:\n{response['answer']}")
            
            if response['sources']:
                print(f"\nSources:")
                for source in response['sources']:
                    print(f"  - {source}")
        
        print("\n" + "="*70)
        print("All tests completed!")
        print("="*70)
        
    except Exception as e:
        print(f"\nError: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())