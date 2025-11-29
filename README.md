\# 📚 Company Knowledge Base Chatbot



An AI-powered chatbot that answers employee questions using company documents through RAG (Retrieval Augmented Generation).



!\[Python](https://img.shields.io/badge/Python-3.11-blue)

!\[Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)

!\[License](https://img.shields.io/badge/License-MIT-green)



\## 🎯 Features



\- \*\*Intelligent Q\&A\*\*: Ask questions in natural language and get accurate answers

\- \*\*Source Attribution\*\*: Every answer cites the specific company documents used

\- \*\*Semantic Search\*\*: Finds relevant information even when exact keywords don't match

\- \*\*Chat History\*\*: Maintains conversation context for follow-up questions

\- \*\*Local Processing\*\*: Runs entirely on your machine - no data sent to external APIs



\## 🏗️ Architecture

```

User Question

&nbsp;    ↓

Semantic Search (ChromaDB)

&nbsp;    ↓

Retrieve Relevant Documents

&nbsp;    ↓

Generate Answer (Ollama + LLM)

&nbsp;    ↓

Cited Response

```



\*\*Tech Stack:\*\*

\- \*\*LLM\*\*: Ollama (Llama 2) - Local AI model

\- \*\*Vector DB\*\*: ChromaDB - Document embeddings \& search

\- \*\*Framework\*\*: LangChain - RAG pipeline

\- \*\*UI\*\*: Streamlit - Web interface

\- \*\*Language\*\*: Python 3.11



\## 🚀 Quick Start



\### Prerequisites



\- Python 3.11+

\- Anaconda/Miniconda

\- Ollama installed (\[download here](https://ollama.ai))



\### Installation



1\. \*\*Clone the repository\*\*

```bash

&nbsp;  git clone https://github.com/YOUR\_USERNAME/company-kb-chatbot.git

&nbsp;  cd company-kb-chatbot

```



2\. \*\*Create conda environment\*\*

```bash

&nbsp;  conda create -n company-kb python=3.11 -y

&nbsp;  conda activate company-kb

```



3\. \*\*Install dependencies\*\*

```bash

&nbsp;  pip install -r requirements.txt

```



4\. \*\*Install Ollama model\*\*

```bash

&nbsp;  ollama pull llama2

```



5\. \*\*Index your documents\*\*

```bash

&nbsp;  python scripts/index\_documents.py

```



6\. \*\*Run the app\*\*

```bash

&nbsp;  streamlit run src/app.py

```



Visit `http://localhost:8501` in your browser! 🎉



\## 📁 Project Structure

```

company-kb-chatbot/

├── src/

│   ├── document\_processor.py  # Document loading \& chunking

│   ├── vector\_store.py         # ChromaDB management

│   ├── chatbot.py              # RAG chatbot logic

│   └── app.py                  # Streamlit UI

├── data/

│   ├── documents/              # Company policy documents

│   └── chroma\_db/              # Vector database (auto-generated)

├── scripts/

│   └── index\_documents.py      # Document indexing script

├── requirements.txt

└── README.md

```



\## 💡 Usage



\### Adding New Documents



1\. Place PDF or TXT files in `data/documents/`

2\. Re-run indexing:

```bash

&nbsp;  python scripts/index\_documents.py --force

```



\### Sample Questions



\- "How many vacation days do I get after 3 years?"

\- "What is the remote work policy?"

\- "How do I submit an expense report?"

\- "What are the paid holidays?"



\## 🔧 Configuration



Edit `.env` to customize:

```bash

OLLAMA\_MODEL=llama2           # Change AI model

CHROMA\_PERSIST\_DIR=./data/chroma\_db

COLLECTION\_NAME=company\_docs

```



\## 🎨 Features in Detail



\### RAG (Retrieval Augmented Generation)



1\. \*\*Document Processing\*\*: Splits documents into 500-character chunks with 50-character overlap

2\. \*\*Vector Embeddings\*\*: Converts text to numerical representations for semantic search

3\. \*\*Semantic Search\*\*: Finds relevant chunks based on meaning, not just keywords

4\. \*\*Context-Aware Responses\*\*: LLM generates answers using only retrieved context

5\. \*\*Source Attribution\*\*: Tracks which documents were used for each answer



\### UI Features



\- 💬 Interactive chat interface

\- 📎 Source citations for transparency

\- 💡 Sample questions for quick start

\- 📊 Knowledge base statistics

\- 🗑️ Clear chat history

\- 📱 Responsive design



\## 🧪 Testing



Run individual components:

```bash

\# Test document processor

python src/document\_processor.py



\# Test vector store

python src/vector\_store.py



\# Test chatbot

python src/chatbot.py

```



\## 📈 Future Enhancements



\- \[ ] Support for more document formats (Word, Excel)

\- \[ ] Admin panel for document management

\- \[ ] Multi-user authentication

\- \[ ] Conversation export

\- \[ ] Advanced analytics dashboard

\- \[ ] Integration with Claude API for better responses



\## 🐛 Troubleshooting



\*\*Ollama not found:\*\*

```bash

\# Check if Ollama is installed

ollama --version



\# Make sure it's in your PATH

```



\*\*Slow responses:\*\*

\- Normal! Local LLM processing takes 1-2 minutes per response

\- Consider using a faster model: `ollama pull phi`



\*\*Empty knowledge base:\*\*

```bash

\# Re-run indexing

python scripts/index\_documents.py --force

```



\## 📝 License



MIT License - feel free to use this project for learning or as a foundation for your own chatbot!



\## 🤝 Contributing



This is a portfolio project, but suggestions are welcome! Feel free to:

\- Open issues for bugs

\- Suggest new features

\- Share your implementations



\## 👨‍💻 Author



\*\*Oluwagbemiga Nelson Ajayi\*\*

\- GitHub: \[@nelsonajayi](https://github.com/nelsonajayi)

\- LinkedIn: (https://linkedin.com/in/oluwagbemiga-ajayi-phd-28565b90)



\## 🙏 Acknowledgments



\- \[Ollama](https://ollama.ai) for local LLM capabilities

\- \[ChromaDB](https://www.trychroma.com/) for vector storage

\- \[LangChain](https://www.langchain.com/) for RAG framework

\- \[Streamlit](https://streamlit.io/) for the amazing UI framework



---



\*\*⭐ If you found this helpful, please star the repository!\*\*

