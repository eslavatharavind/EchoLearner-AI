# 🚀 Quick Start Guide - EchoLearn AI

Get up and running in 5 minutes!

## Prerequisites
- Python 3.9+ installed
- OpenAI API key (or Groq API key for free alternative)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages. Installation takes about 5-10 minutes.

### 2. Configure API Keys

Create a `.env` file in the project root by copying the example:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Don't have an OpenAI key? Use Groq (FREE):**

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-api-key-here
TTS_PROVIDER=gtts
```

Get a free Groq API key at: https://console.groq.com

### 3. Start the Backend

```bash
python server.py
```

Wait for: `✓ EchoLearn AI Server started successfully`

### 4. Start the Frontend (New Terminal)

Open a new terminal window and run:

```bash
streamlit run app.py
```

Your browser will open automatically to `http://localhost:8501`

## First Steps

### Upload a Document

1. In the sidebar, click "Browse files"
2. Select a PDF or Jupyter Notebook
3. Click "📤 Process Document"
4. Wait for processing to complete

### Ask Your First Question

**Option 1: Voice**
1. Go to the "🎤 Voice Input" tab
2. Click the microphone button
3. Ask a question (e.g., "What is this document about?")
4. Listen to the tutor's response

**Option 2: Text**
1. Go to the "⌨️ Text Input" tab
2. Type your question
3. Click "🚀 Ask"
4. Read or listen to the answer

## Example Usage

### With a Machine Learning PDF:
1. Upload `machine_learning_basics.pdf`
2. Ask: "What is supervised learning?"
3. Get a simple, step-by-step explanation

### With a Python Notebook:
1. Upload `data_analysis.ipynb`
2. Ask: "Explain the pandas code"
3. Get code explanations with examples

## Troubleshooting

### "Backend server is not running"
- Make sure `python server.py` is running in another terminal
- Check for error messages in the server terminal

### "Configuration errors: OpenAI API key required"
- Verify your `.env` file exists
- Check that `OPENAI_API_KEY` is set correctly
- Make sure there are no extra spaces

### "Module not found" errors
- Run `pip install -r requirements.txt` again
- Make sure you're in the project directory

## Configuration Options

### Use Free/Open-Source Stack

Edit `.env`:

```env
# Free LLM via Groq
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-key

# Free TTS
TTS_PROVIDER=gtts

# Local STT (already free)
STT_PROVIDER=faster-whisper
STT_MODEL=base

# Free embeddings (already default)
EMBEDDING_PROVIDER=sentence-transformers
```

### Faster Processing

Use smaller models:

```env
STT_MODEL=tiny
CHUNK_SIZE=300
```

### Better Quality

Use larger models (slower):

```env
STT_MODEL=medium
OPENAI_MODEL=gpt-4
LLM_TEMPERATURE=0.7
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore API endpoints at http://localhost:8000/docs
- Customize the tutor personality in `prompt.py`
- Adjust chunking parameters in `.env`

## Common Questions

**Q: Can I use this offline?**
A: Partially. STT (Faster-Whisper) and embeddings work offline, but LLM (OpenAI/Groq) requires internet.

**Q: How much does it cost?**
A: Using Groq + gTTS is completely FREE. OpenAI GPT-4 + TTS costs ~$0.01-0.05 per question.

**Q: What document types are supported?**
A: Currently PDF (.pdf) and Jupyter Notebook (.ipynb). More formats coming soon!

**Q: How many documents can I upload?**
A: Unlimited! Documents are chunked and stored in the vector database.

**Q: Can I clear the database?**
A: Yes, use the "Clear Index" endpoint or check the "Rebuild index" box when uploading.

## Support

- Check [README.md](README.md) for detailed troubleshooting
- Review configuration in `.env`
- Ensure all dependencies are installed

---

**Happy Learning! 🎓**
