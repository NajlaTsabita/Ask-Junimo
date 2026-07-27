# Ask Junimo — Stardew Valley AI Assistant

An AI-powered conversational assistant that helps Stardew Valley players look up game mechanics, NPC gift preferences, crop schedules, and item details — grounded in real wiki data using Retrieval-Augmented Generation (RAG).

---

## Overview

Ask Junimo is a domain-specific chatbot built for Stardew Valley players. It uses Retrieval-Augmented Generation (RAG) to pull context directly from the Stardew Valley Wiki instead of relying on the LLM's memory alone, so answers stay accurate and grounded rather than hallucinated.

On top of that, Ask Junimo also knows **your own farm**. On first launch you fill in a short form (player name, farm type, current season, gold, skill levels, etc.), and Junimo Bot uses that context to personalize its answers — for example, prioritizing crops that fit your *current* season instead of giving generic advice.

Whether you want to check a crop's growth cycle, find out what a villager loves as a gift, plan Community Center bundles, or figure out what fish are biting this season, Ask Junimo gives you a fast, contextual answer.

---

## Key Features

- **Domain-specific knowledge base** — answers grounded in the official Stardew Valley Wiki (crops, NPC gifts, schedules, fishing, mining, crafting, festivals).
- **Retrieval-Augmented Generation (RAG)** — combines vector similarity search with an LLM so answers are backed by real wiki content, not guesses.
- **Personalized player context** — your own farm data (season, gold, skills, farm type, pet, etc.) is injected into every answer, so suggestions actually fit your save file.
- **Persistent player data** — fill in your farm details once; they're saved locally and reloaded automatically every time you run the app. Editable anytime from the sidebar.
- **Streaming chat UI** — clean Streamlit interface with real-time streamed responses and a live player-stats sidebar.

---

## Tech Stack & Architecture

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| RAG / LLM orchestration | [LangChain](https://python.langchain.com/) (`langchain`, `langchain-community`) |
| LLM | [Groq](https://groq.com/) — `openai/gpt-oss-120b` via `langchain-groq` |
| Embeddings | Google Generative AI — `gemini-embedding-001` via `langchain-google-genai` |
| Vector database | [ChromaDB](https://www.trychroma.com/) (persisted locally to `data/vectorstore`) |
| Player data storage | SQLite (`data/player.db`), stdlib `sqlite3` |
| Document source | Stardew Valley Wiki PDF (`data/Stardew_Valley_Wiki.pdf`), parsed with `pypdf` |
| UI | Streamlit |

---

## Getting Started

### Prerequisites
- Python 3.10+
- Git
- A [Groq API key](https://console.groq.com/keys)
- A [Google AI (Gemini) API key](https://aistudio.google.com/apikey) for embeddings

### 1. Clone the repository
```bash
git clone https://github.com/NajlaTsabita/Ask-Junimo.git
cd Ask-Junimo
```

### 2. Set up a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### 5. Run the application
```bash
streamlit run app.py
```

On first launch, you'll see a short onboarding form to set up your farm — that's expected, not an error. Fill it in once and you're good to go.

---

## Your Player Data

Unlike earlier versions of this project (which auto-generated a random player profile), Ask Junimo now uses **your real farm data**, entered once through a form and stored locally:

- **First run:** since no data exists yet, you'll get an onboarding screen asking for your player name, farm name, farm type, current season/year, gold, favorite thing, pet, skill levels, and house upgrade level.
- **Every run after that:** your data is loaded automatically from `data/player.db` — no need to fill the form again.
- **Editing:** open the **"Edit Data Player"** section in the sidebar at any time to update your stats as your save file progresses.
- **Resetting:** the **"Reset Data Player"** button in the sidebar clears your saved data and brings back the onboarding form.

This data is stored **locally only**, in a SQLite file (`data/player.db`) inside the project folder — it isn't sent anywhere except as context in your chat prompts to the LLM.

---

## How the RAG System Works

1. **Document processing** — `data/Stardew_Valley_Wiki.pdf` is loaded and split into ~2000-character text chunks.
2. **Embedding & storage** — each chunk is converted into a vector embedding (`gemini-embedding-001`) and stored in a local ChromaDB vector store (`data/vectorstore`).
3. **Information retrieval** — when you ask a question (e.g. *"What are Abigail's loved gifts?"*), the app runs a similarity search against ChromaDB to pull the most relevant wiki chunks.
4. **Contextual generation** — those chunks, your saved player data, and the conversation history are all injected into the prompt sent to the LLM (Groq), which streams back a grounded, in-character answer as Junimo Bot.

---

## Project Structure

```
Ask-Junimo/
├── app.py              # Entry point: init DB, load/collect player data, wire up RAG chain, launch UI
├── assistant.py         # Assistant class: builds the LangChain RAG pipeline (retriever + prompt + LLM)
├── gui.py               # Streamlit UI: sidebar (player stats, edit/reset), chat rendering
├── player_form.py        # Onboarding & edit form for player data
├── prompts.py            # System prompt (Junimo Bot persona) and welcome message
├── requirements.txt
├── data/
│   ├── database.py       # SQLite persistence layer for player data
│   ├── Stardew_Valley_Wiki.pdf   # RAG knowledge source
│   ├── player.db          # Created on first run — your saved farm data (gitignored)
│   └── vectorstore/        # Created on first run — cached Chroma embeddings (gitignored)
├── streamlit/
│   ├── config.toml       # Custom Streamlit UI theme configuration
└── .env                  # Your API keys (gitignored)
```

---

Developed by [Najla Tsabita](https://github.com/NajlaTsabita).
