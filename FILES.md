# EchoLearn AI - Project Files

## Core Files (17 Python Modules)

### Configuration & Setup
- `config.py` - Central configuration management with environment variables
- `requirements.txt` - All Python dependencies
- `.env.example` - Example environment variables (copy to .env)
- `check_system.py` - System verification script

### Document Ingestion (5 modules)
- `pdf_loader.py` - Extract text from PDF files (PyMuPDF + pdfplumber)
- `notebook_loader.py` - Parse Jupyter Notebooks (.ipynb)
- `text_cleaner.py` - Clean and normalize extracted text
- `chunker.py` - Split text into chunks with overlap
- `build_vector_db.py` - Build FAISS vector database with embeddings

### RAG System (4 modules)
- `retriever.py` - Retrieve relevant chunks from vector database
- `prompt.py` - Tutor personality and prompt templates
- `tutor_agent.py` - Main RAG agent (LLM + retrieval + memory)
- `memory.py` - Conversation history management

### Speech Processing (2 modules)
- `speech_to_text.py` - Voice → Text using Faster-Whisper
- `text_to_speech.py` - Text → Voice using OpenAI TTS / gTTS

### Application Servers (2 modules)
- `server.py` - FastAPI backend with REST API
- `app.py` - Streamlit frontend web interface

### Documentation
- `README.md` - Complete project documentation
- `QUICKSTART.md` - Quick setup guide
- `FILES.md` - This file

## Data Directories (Auto-created)

```
data/
├── uploads/          # Uploaded PDF and notebook files
├── vector_db/        # FAISS index and document store
│   ├── faiss_index.bin
│   └── documents.pkl
├── audio_output/     # Generated TTS audio files
└── logs/            # Application logs
```

## File Dependencies

### Entry Points
- **Backend**: `server.py` imports everything
- **Frontend**: `app.py` calls backend API

### Module Dependencies

```
server.py
  ├── config.py
  ├── pdf_loader.py
  ├── notebook_loader.py
  ├── text_cleaner.py
  ├── chunker.py
  ├── build_vector_db.py
  ├── tutor_agent.py
  │   ├── retriever.py
  │   │   └── build_vector_db.py
  │   ├── prompt.py
  │   ├── memory.py
  │   └── config.py
  ├── speech_to_text.py
  └── text_to_speech.py

app.py
  └── (Makes HTTP requests to server.py)
```

## File Sizes (Approximate)

| File | Lines | Size |
|------|-------|------|
| config.py | 150 | 6 KB |
| server.py | 350 | 14 KB |
| app.py | 300 | 12 KB |
| tutor_agent.py | 250 | 10 KB |
| build_vector_db.py | 200 | 8 KB |
| retriever.py | 180 | 7 KB |
| speech_to_text.py | 150 | 6 KB |
| text_to_speech.py | 180 | 7 KB |
| Others | ~150 each | ~6 KB each |
| **Total** | ~2500 | ~100 KB |

## Key Configuration Files

### .env (User creates from .env.example)
```env
OPENAI_API_KEY=your_key
LLM_PROVIDER=openai
TTS_PROVIDER=openai
STT_MODEL=base
CHUNK_SIZE=500
```

### requirements.txt
- 40+ packages
- Total download: ~2-3 GB (includes PyTorch)
- Installation time: 5-10 minutes

## Usage Flow

```
1. User runs: python server.py
   → Loads config.py
   → Initializes all modules
   → Starts FastAPI server on port 8000

2. User runs: streamlit run app.py
   → Opens browser to localhost:8501
   → Connects to backend API

3. User uploads document (app.py → server.py)
   → pdf_loader or notebook_loader extracts text
   → text_cleaner cleans it
   → chunker splits into chunks
   → build_vector_db creates embeddings
   → Saves to data/vector_db/

4. User asks question (voice or text)
   → speech_to_text (if voice input)
   → retriever searches vector_db
   → tutor_agent generates answer using LLM
   → text_to_speech generates audio
   → Returns to frontend
```

## Optional Files You May Create

- `.env` - Your actual environment variables (don't commit!)
- `sample.pdf` - Test PDF document
- `sample.ipynb` - Test Jupyter Notebook
- `test_*.py` - Your custom test scripts

## Files to Ignore (Not included)

- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python
- `venv/` or `env/` - Virtual environment
- `.env` - Your API keys (keep private!)
- `data/` - Generated data (large)

## Total Project Size

- **Code**: ~100 KB
- **Dependencies**: ~2-3 GB (PyTorch, Transformers, etc.)
- **Data** (after use): Varies by documents uploaded
  - Example: 10 PDFs → ~50 MB vector database
  - Audio files: ~1 MB per minute of speech

## Customization Points

Want to modify behavior? Edit these files:

- **Tutor personality**: `prompt.py` → Change SYSTEM_PROMPT
- **Chunking strategy**: `chunker.py` → Adjust separators
- **Retrieval settings**: `config.py` → RETRIEVAL_TOP_K
- **Voice settings**: `text_to_speech.py` → _add_teaching_pauses
- **UI design**: `app.py` → Custom CSS

## Verification

Run the system check:
```bash
python check_system.py
```

This verifies:
- Python version
- All files present
- Dependencies installed
- Modules can be imported
- Basic functionality works
