# Ask Junimo - Stardew Valley AI Assistant

An AI-powered conversational assistant designed to help Stardew Valley players query game mechanics, NPC preferences, crops, schedules, and item details using Retrieval-Augmented Generation (RAG).

=====================================
OVERVIEW
=====================================
Ask Junimo is a domain-specific AI chatbot built specifically for Stardew Valley players. Utilizing Retrieval-Augmented Generation (RAG), the application retrieves context directly from official game wiki data and guides to provide accurate, hallucination-free answers to player queries in real time.

Whether you need to check crop growth cycles, determine NPC gift preferences, optimize bundle completion in the Community Center, or locate specific fish during seasonal weather conditions, Ask Junimo delivers precise and contextually relevant responses.

=====================================
2. KEY FEATURES
=====================================
- Domain-Specific Knowledge Base: Answers queries related to crops, NPC loved gifts, villager schedules, fish locations, mining, crafting, and festival events.
- Retrieval-Augmented Generation (RAG): Combines vector search retrieval with Large Language Models (LLMs) to ensure high factual accuracy based on official game data.
- Fast Semantic Search: Uses vector embeddings for high-precision context extraction and fast response retrieval.
- Interactive Chat Interface: Clean and intuitive user interface optimized for quick lookups during gameplay.

=====================================
3. TECH STACK & ARCHITECTURE
=====================================
- Language: Python 3.9+
- RAG & AI Framework: LangChain / LlamaIndex
- Embedding Model: OpenAI Embeddings / HuggingFace Sentence Transformers
- Vector Database: ChromaDB / FAISS / Qdrant
- LLM Integration: OpenAI GPT / Google Gemini / Ollama
- User Interface: Streamlit / Gradio / React

=====================================
4. GETTING STARTED
=====================================
Prerequisites:
  - Python 3.9+
  - Git

Clone the Repository:
  git clone https://github.com/NajlaTsabita/Ask-Junimo.git
  cd Ask-Junimo

Set Up Virtual Environment:
  # Windows
  python -m venv venv
  venv\Scripts\activate

  # macOS / Linux
  python3 -m venv venv
  source venv/bin/activate

Install Dependencies:
  pip install -r requirements.txt

Configure Environment Variables (.env):
  OPENAI_API_KEY=your_openai_api_key_here

Run the Application:
  streamlit run app.py

=====================================
5. HOW THE RAG SYSTEM WORKS
=====================================

1. Document Processing: Stardew Valley reference data and wiki guides are chunked into structured text segments.
2. Embedding & Storage: Text chunks are converted into dense vector embeddings and stored in a vector database.
3. Information Retrieval: When a user submits a question (e.g., "What are Abigail's loved gifts?"), the system executes a similarity search to find the most relevant context chunks.
4. Contextual Generation: Retrieved facts are injected into the prompt context provided to the LLM to generate an accurate, grounded response.


Developed by Najla Tsabita (https://github.com/NajlaTsabita).
