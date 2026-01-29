# 🎓 EchoLearn AI - Universal Voice Tutor Agent

**EchoLearn AI** is a complete end-to-end Python voice tutor system that allows users to upload PDF files or Jupyter Notebooks and ask questions via voice or text, receiving spoken human-like explanations powered by Retrieval-Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## ✨ Features

### 🎤 Voice Interaction
- **Speech-to-Text**: Convert voice questions to text using Faster-Whisper (local, no API key needed)
- **Text-to-Speech**: Get answers in natural human-like voice (OpenAI TTS, gTTS, or Coqui TTS)
- **Teaching-Style Delivery**: Automatic pauses between sentences for better comprehension

### 📚 Document Processing
- **PDF Support**: Extract and index content from PDF textbooks and documents
- **Jupyter Notebook Support**: Parse notebooks including code, markdown, and comments
- **Smart Chunking**: Semantic text chunking with overlap for better context

### 🧠 RAG-Powered Tutoring
- **Context-Aware Answers**: Uses retrieved document context to provide accurate responses
- **Conversation Memory**: Maintains context across multiple questions
- **Patient Teacher Personality**: Simple language, real-life examples, step-by-step explanations

### 🎯 Flexible Configuration
- **Multiple LLM Providers**: OpenAI GPT, Groq (Llama), Mistral
- **Multiple TTS Providers**: OpenAI TTS, gTTS (free), Coqui TTS
- **Vector Database**: FAISS (local, fast) with option for Chroma
- **Customizable Parameters**: Chunk size, retrieval settings, model selection

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                       │
│              (Voice/Text Input, Audio Playback)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP API
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Document   │  │    Speech    │  │     RAG      │      │
│  │  Ingestion   │  │  Processing  │  │   Tutor      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    FAISS     │    │    Whisper   │    │  OpenAI/Groq │
│ Vector DB    │    │     STT      │    │     LLM      │
└──────────────┘    └──────────────┘    └──────────────┘
```

### RAG Pipeline

1. **Document Ingestion**: PDF/Notebook → Text Extraction → Cleaning → Chunking
2. **Indexing**: Chunks → Embeddings → FAISS Vector Store
3. **Query Processing**: Voice/Text → STT → Question
4. **Retrieval**: Question → Vector Search → Top-K Relevant Chunks
5. **Generation**: Context + Question → LLM → Answer
6. **Response**: Answer → TTS → Audio

---

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern web framework for building APIs
- **LangChain**: RAG orchestration and document processing
- **FAISS**: Fast vector similarity search
- **Faster-Whisper**: Efficient speech recognition
- **SentenceTransformers**: Document embeddings

### Frontend
- **Streamlit**: Interactive web interface
- **audio-recorder-streamlit**: Voice recording widget

### AI/ML Services
- **OpenAI GPT-4**: LLM for responses (configurable)
- **Groq**: Fast LLM inference (alternative)
- **OpenAI TTS**: Natural text-to-speech (configurable)
- **gTTS**: Free text-to-speech (alternative)

### Document Processing
- **PyMuPDF**: PDF text extraction
- **pdfplumber**: PDF processing (fallback)
- **nbformat**: Jupyter Notebook parsing

---

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- (Optional) GPU for faster speech processing

### Step 1: Clone or Download Project

```bash
cd EchoLearner-AI
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

> [!IMPORTANT]
> **Windows Users**: If you encounter errors with `faiss-cpu`, `torch`, or `tensorflow`, try installing `tf-keras` and ensuring your environment is up to date:
> ```bash
> pip install tf-keras
> ```

**Note**: Installation may take several minutes due to large packages (PyTorch, Transformers, etc.)

### Step 4: Configure Environment

Copy the example environment file and add your API keys:

```bash
copy .env.example .env
```

Edit `.env` file with your preferred text editor and add your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here  # Optional
```

---

## ⚙️ Configuration

### Environment Variables

The `.env` file controls all configuration. Key settings:

#### LLM Provider
```env
LLM_PROVIDER=openai  # Options: openai, groq
OPENAI_MODEL=gpt-4
LLM_TEMPERATURE=0.7
```

#### TTS Provider
```env
TTS_PROVIDER=openai  # Options: openai, gtts (free)
TTS_VOICE=alloy  # For OpenAI: alloy, echo, fable, onyx, nova, shimmer
```

#### STT Configuration
```env
STT_PROVIDER=faster-whisper  # Local, no API key needed
STT_MODEL=base  # Options: tiny, base, small, medium, large
```

#### Embedding & Vector DB
```env
EMBEDDING_PROVIDER=sentence-transformers  # No API key needed
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_DB_TYPE=faiss
```

#### Chunking Parameters
```env
CHUNK_SIZE=500
CHUNK_OVERLAP=100
```

### Provider Options

| Feature | Free Option | Paid Option | Recommendation |
|---------|-------------|-------------|----------------|
| **LLM** | Groq (free tier) | OpenAI GPT-4 | OpenAI for quality |
| **TTS** | gTTS | OpenAI TTS | OpenAI for natural voice |
| **STT** | Faster-Whisper | OpenAI Whisper | Faster-Whisper (local) |
| **Embeddings** | SentenceTransformers | OpenAI Embeddings | SentenceTransformers |

---

## 🚀 Usage

### Starting the Application

#### Step 1: Start the Backend Server

1. Open a terminal in the project root.
2. Run the server:
   ```bash
   python server.py
   ```
3. Wait for the message: `✓ EchoLearn AI Server started successfully`

#### Step 2: Start the Frontend (Vite/React)

1. Open a **new** terminal window.
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install frontend dependencies (if first time):
   ```bash
   npm install
   ```
4. Start the dev server:
   ```bash
   npm run dev
   ```
5. The app will be available at: **[http://localhost:3000](http://localhost:3000)**

### Using the Application

#### 1. Upload Documents
- Click "📚 Document Upload" in the sidebar
- Choose a PDF or Jupyter Notebook file
- Click "📤 Process Document"
- Wait for processing to complete

#### 2. Ask Questions

**Via Voice:**
- Go to "🎤 Voice Input" tab
- Click the microphone icon to record
- Ask your question clearly
- Click stop when finished
- Listen to the tutor's audio response

**Via Text:**
- Go to "⌨️ Text Input" tab
- Type your question
- Click "🚀 Ask"
- Read the answer and/or listen to audio

### Example Questions

After uploading a machine learning PDF:
- "What is supervised learning?"
- "Can you explain gradient descent with an example?"
- "What's the difference between classification and regression?"

After uploading a Python notebook:
- "Explain this code step by step"
- "What does this function do?"
- "Can you show me a simpler example?"

---

## 📡 API Documentation

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "vector_db": true,
    "tutor_agent": true,
    "stt": true,
    "tts": true
  },
  "vector_db_stats": {
    "num_documents": 42
  }
}
```

### Upload Document
```http
POST /upload
Content-Type: multipart/form-data

file: <PDF or IPYNB file>
rebuild_index: false
```

**Response:**
```json
{
  "status": "success",
  "filename": "textbook.pdf",
  "num_chunks": 35,
  "total_documents_in_index": 42,
  "processing_time": 12.5
}
```

### Ask Question (Text)
```http
POST /ask
Content-Type: multipart/form-data

text: "What is machine learning?"
use_retrieval: true
return_audio: true
```

**Response:**
```json
{
  "status": "success",
  "question": "What is machine learning?",
  "answer": "Machine learning is...",
  "audio_path": "/path/to/audio.mp3",
  "num_sources": 3,
  "timing": {
    "agent_time": 2.3,
    "synthesis_time": 1.1
  }
}
```

### Ask Question (Audio)
```http
POST /ask
Content-Type: multipart/form-data

audio: <WAV audio file>
use_retrieval: true
return_audio: true
```

---

## 📁 Project Structure

```
EchoLearner-AI/
│
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
│
├── server.py                # FastAPI backend server
├── app.py                   # Streamlit frontend
│
├── pdf_loader.py            # PDF document loader
├── notebook_loader.py       # Jupyter Notebook loader
├── text_cleaner.py          # Text preprocessing
├── chunker.py               # Text chunking with overlap
├── build_vector_db.py       # FAISS vector database builder
│
├── retriever.py             # Document retrieval from vector DB
├── prompt.py                # Tutor personality prompts
├── tutor_agent.py           # Main RAG tutor agent
├── memory.py                # Conversation memory
│
├── speech_to_text.py        # Voice → Text (Faster-Whisper)
├── text_to_speech.py        # Text → Voice (OpenAI/gTTS)
│
└── data/                    # Auto-created data directory
    ├── uploads/             # Uploaded documents
    ├── vector_db/           # FAISS index
    └── audio_output/        # Generated audio files
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Server Won't Start
**Error**: `Configuration errors: OpenAI API key required`

**Solution**: 
- Make sure you created `.env` file from `.env.example`
- Add valid `OPENAI_API_KEY` to `.env`
- Or change `LLM_PROVIDER=groq` and add `GROQ_API_KEY`

#### 2. Module Not Found
**Error**: `ModuleNotFoundError: No module named 'faster_whisper'`

**Solution**:
```bash
pip install -r requirements.txt
```

#### 3. FAISS Import Error
**Error**: `ImportError: DLL load failed while importing faiss`

**Solution** (Windows):
```bash
pip uninstall faiss-cpu
pip install faiss-cpu --no-cache
```

#### 4. Slow Transcription
**Issue**: Speech-to-text takes too long

**Solution**: Use smaller Whisper model
```env
STT_MODEL=tiny  # or base (instead of medium/large)
```

#### 5. Audio Playback Not Working
**Issue**: Can't hear generated audio

**Solution**:
- Check browser audio permissions
- Try downloading audio file directly
- Verify TTS provider is configured correctly

### Performance Tips

1. **Faster Indexing**: Use smaller chunk size
   ```env
   CHUNK_SIZE=300
   ```

2. **Better Quality**: Use larger Whisper model (if you have GPU)
   ```env
   STT_MODEL=medium
   ```

3. **Cost Savings**: Use free alternatives
   ```env
   LLM_PROVIDER=groq
   TTS_PROVIDER=gtts
   ```

---

## 🧪 Testing

### Test Document Ingestion

```bash
python -c "
from pdf_loader import PDFLoader
from chunker import TextChunker

loader = PDFLoader()
chunker = TextChunker()

# Test with your PDF
text = loader.load('sample.pdf')
chunks = chunker.chunk(text)
print(f'Created {len(chunks)} chunks')
"
```

### Test Speech Pipeline

```bash
python speech_to_text.py  # Should load model
python text_to_speech.py  # Should initialize TTS
```

### Test RAG Agent

```bash
python tutor_agent.py  # Should initialize successfully
```

---

## 🔒 API Keys

### Getting API Keys

#### OpenAI (Recommended)
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up / Log in
3. Navigate to API Keys
4. Create new secret key
5. Add to `.env` as `OPENAI_API_KEY`

#### Groq (Free Alternative)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for free account
3. Get API key
4. Add to `.env` as `GROQ_API_KEY`
5. Set `LLM_PROVIDER=groq`

---

## 📝 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Support

For issues and questions:
- Create an issue on GitHub
- Check the Troubleshooting section
- Review configuration documentation

---

## 🎯 Future Enhancements

- [ ] Support for more document types (DOCX, HTML, Markdown)
- [ ] Multi-language support
- [ ] Fine-tuned models for specific domains
- [ ] Real-time streaming responses
- [ ] Mobile app interface
- [ ] Multi-modal input (images, diagrams)
- [ ] Collaborative learning sessions

---

## 🙏 Acknowledgments

Built with:
- [LangChain](https://langchain.com) - RAG framework
- [FastAPI](https://fastapi.tiangolo.com) - Backend framework  
- [Streamlit](https://streamlit.io) - Frontend framework
- [OpenAI](https://openai.com) - LLM and TTS
- [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) - Speech recognition
- [FAISS](https://github.com/facebookresearch/faiss) - Vector search

---

**Made with ❤️ for Learners Everywhere**
