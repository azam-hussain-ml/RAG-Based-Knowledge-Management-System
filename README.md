# RAG-Based Knowledge Management System

<div align="center">

**An enterprise-grade Retrieval-Augmented Generation pipeline that answers questions strictly from your documents — no hallucinations, no guesswork.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C?style=flat-square)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--Turbo-412991?style=flat-square&logo=openai&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-000000?style=flat-square&logo=flask&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-FF6B35?style=flat-square)
![AWS](https://img.shields.io/badge/AWS-S3-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>

---

## Overview

Most AI assistants generate responses from general training data — which means they hallucinate, fabricate citations, and confidently give wrong answers.

This system is different.

The RAG-Based Knowledge Management System is a **document-grounded AI assistant** built on a production-level Retrieval-Augmented Generation architecture. It ingests your private documents, indexes them into a local vector database, and at query time retrieves only the most semantically relevant chunks — which are then passed as grounded context to GPT-3.5-Turbo.

The result: every answer is traceable back to your source material. Nothing is invented.

I built this end-to-end — architecture decisions, debugging version conflicts, resolving SSL certificate issues in conda environments, migrating from deprecated LangChain APIs to the modern LCEL pipeline. Every layer was intentional.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    INGESTION PIPELINE                   │
│                                                         │
│  PDF / TXT File                                         │
│       │                                                 │
│       ▼                                                 │
│  PyPDFLoader / TextLoader                               │
│       │                                                 │
│       ▼                                                 │
│  RecursiveCharacterTextSplitter                         │
│  chunk_size=1000  │  chunk_overlap=200                  │
│       │                                                 │
│       ▼                                                 │
│  OpenAI Embeddings (text-embedding-ada-002)             │
│  1536-dimensional dense vectors                         │
│       │                                                 │
│       ├──────────────────────────┐                      │
│       ▼                          ▼                      │
│  ChromaDB (local)           AWS S3 (cloud backup)       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                     QUERY PIPELINE                      │
│                                                         │
│  User Question                                          │
│       │                                                 │
│       ▼                                                 │
│  OpenAI Embeddings → query vector                       │
│       │                                                 │
│       ▼                                                 │
│  ChromaDB similarity search → top-k=4 chunks           │
│       │                                                 │
│       ▼                                                 │
│  create_retrieval_chain (LangChain LCEL)                │
│       │                                                 │
│       ▼                                                 │
│  GPT-3.5-Turbo (context-grounded generation)           │
│       │                                                 │
│       ▼                                                 │
│  RunnableWithMessageHistory (session memory)            │
│       │                                                 │
│       ▼                                                 │
│  Answer — sourced exclusively from your documents       │
└─────────────────────────────────────────────────────────┘
```

---

## Key Features

**Document Ingestion**
- Multi-file upload with drag-and-drop interface
- Supports PDF and TXT formats
- Semantic chunking with 200-token overlap to preserve cross-chunk context
- Real-time ingestion status feedback

**Vector Search**
- OpenAI `text-embedding-ada-002` — 1536-dimensional embeddings
- ChromaDB local vector store with cosine similarity search
- Top-4 chunk retrieval per query for optimal context density

**Conversational AI**
- GPT-3.5-Turbo with strict document-grounding prompt
- Full session memory via `RunnableWithMessageHistory`
- Context window preserved across multi-turn conversations

**Storage & Reliability**
- AWS S3 integration for original file backup
- Local ChromaDB persistence across sessions
- Graceful error handling throughout the pipeline

**Frontend**
- Custom dark-themed UI built from scratch
- No CSS frameworks — pure HTML/CSS/JS
- Responsive chat interface with typing indicators

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10 | Core runtime |
| Web Framework | Flask 2.3 | REST API & routing |
| LLM | OpenAI GPT-3.5-Turbo | Answer generation |
| Embeddings | text-embedding-ada-002 | Semantic vectorization |
| Vector Database | ChromaDB | Similarity search & storage |
| RAG Framework | LangChain 0.2 (LCEL) | Pipeline orchestration |
| Cloud Storage | AWS S3 via boto3 | Document backup |
| Document Loaders | PyPDFLoader, TextLoader | File parsing |
| Text Splitting | RecursiveCharacterTextSplitter | Semantic chunking |
| Memory | RunnableWithMessageHistory | Conversation state |
| Frontend | HTML / CSS / JavaScript | Custom UI |

---

## Project Structure

```
rag-knowledge-management/
│
├── app/
│   ├── main.py                      # Flask application & API routes
│   │
│   ├── models/
│   │   └── vector_store.py          # ChromaDB initialization & document indexing
│   │
│   ├── services/
│   │   ├── llm_service.py           # LangChain LCEL RAG pipeline & memory
│   │   └── storage_service.py       # AWS S3 upload & retrieval
│   │
│   ├── templates/
│   │   └── index.html               # Frontend UI (custom dark theme)
│   │
│   └── config.py                    # Environment variable management
│
├── vector_db/                       # ChromaDB persistent storage (auto-generated)
├── .env                             # API keys — not committed to version control
├── requirements.txt                 # Pinned dependencies
└── README.md
```

---

## Local Setup

### Prerequisites
- Python 3.10+
- Conda (recommended) or virtualenv
- OpenAI API key
- AWS account with S3 bucket

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/azam-hussain-ml/RAG-Based-Knowledge-Management-System.git
cd rag-knowledge-management
```

**2. Create isolated environment**
```bash
conda create -n llmapp python=3.10
conda activate llmapp
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=sk-...
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_BUCKET_NAME=your_bucket_name
VECTOR_DB_PATH=./vector_db
```

**5. Fix SSL certificate path (conda environments)**
```bash
conda env config vars set SSL_CERT_FILE="path/to/anaconda3/envs/llmapp/Lib/site-packages/certifi/cacert.pem"
conda deactivate && conda activate llmapp
```

**6. Start the application**
```bash
python app/main.py
```

**7. Open in browser**
```
http://127.0.0.1:8080
```

---

## Usage

**Step 1 — Upload a document**
Drag and drop a PDF or TXT file into the ingestion panel, or click to browse.

**Step 2 — Vectorize**
Click "Ingest & Vectorize". The system parses, chunks, embeds, and indexes the document into ChromaDB. Original file is simultaneously backed up to S3.

**Step 3 — Query**
Type any natural language question. The system retrieves the top-4 most relevant chunks and generates a grounded response using GPT-3.5-Turbo.

**Step 4 — Continue the conversation**
Ask follow-up questions. Session memory preserves full context across the conversation.

---

## Tested Scenarios

| Document Type | Query | Result |
|--------------|-------|--------|
| Professional CV | *"What are this candidate's strongest technical skills?"* | Accurate extraction from experience section |
| Research Paper | *"What problem does this research solve?"* | Precise problem statement retrieval |
| Research Paper | *"What methodology was used in this study?"* | Correct methodology section cited |
| Business Report | *"What were the key findings?"* | Structured summary from document |

---

## Engineering Decisions & Challenges

**LangChain API Migration**
The codebase was originally scaffolded using `ConversationalRetrievalChain`, which was deprecated in LangChain 0.2. I migrated the entire pipeline to the modern LCEL pattern using `create_retrieval_chain`, `create_stuff_documents_chain`, and `RunnableWithMessageHistory` — maintaining identical functionality with a cleaner, more maintainable architecture.

**SSL Certificate Resolution**
Running inside a conda environment caused `SSL_CERT_FILE` to point to a system-level certificate path that did not exist. Resolved by explicitly binding the environment variable to the certifi package path within the active conda environment.

**Chunk Overlap Strategy**
A 200-token overlap between chunks was chosen deliberately. Without overlap, answers to questions that span chunk boundaries are incomplete. The overlap ensures semantic continuity across splits without significant storage overhead.

**Version Pinning**
LangChain's rapid release cycle caused repeated dependency conflicts between `langchain`, `langchain-core`, `langchain-community`, and `langchain-openai`. Resolved by pinning compatible versions (`langchain==0.2.16`, `langchain-core==0.2.38`) and installing with `--no-deps` to bypass resolver conflicts with unrelated packages like `botocore`.

---

## Roadmap

- [ ] Per-chunk source citation in responses
- [ ] DOCX and CSV file support
- [ ] Multi-user authentication with isolated vector namespaces
- [ ] LangSmith tracing for pipeline observability
- [ ] Docker containerization
- [ ] Deployment on AWS EC2 with Nginx reverse proxy
- [ ] Streaming response output (token-by-token)
- [ ] Relevance score display per retrieved chunk

---

## Author

**Azam Hussain**
[LinkedIn](https://www.linkedin.com/in/azam-hussain-681695325)                                          [GitHub](https://github.com/azam-hussain-ml/RAG-Based-Knowledge-Management-System.git)

---

## License

MIT License. See `LICENSE` for details.

---

<div align="center">
<sub>Built from scratch · Every bug debugged manually · No shortcuts taken</sub>
</div>
