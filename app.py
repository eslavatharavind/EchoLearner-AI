"""
Streamlit Frontend for EchoLearn AI - This is the main UI file
User interface for document upload and voice tutoring - Built with Streamlit
"""

import streamlit as st  # Import Streamlit for web interface
import requests  # Import requests to talk to the backend API
from pathlib import Path  # Import Path for file path manipulation
import time  # Import time for delays or timestamps
from audio_recorder_streamlit import audio_recorder  # Import tool to record voice in browser
import base64  # Import base64 for encoding/decoding data
from config import Config  # Import configuration settings

# Configuration
API_BASE_URL = "http://localhost:8000"  # Set the address where the backend server runs

# Page config
st.set_page_config(  # Configure the main web page settings
    page_title="EchoLearn AI - Voice Tutor",  # Set the browser tab title
    page_icon="🎓",  # Set the browser tab icon
    layout="wide",  # Use the full width of the browser screen
    initial_sidebar_state="expanded"  # Keep the sidebar open by default
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {  /* Style for the big main title */
        font-size: 3rem;  /* Make text very large */
        font-weight: bold;  /* Make text bold */
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);  /* Add a purple gradient */
        -webkit-background-clip: text;  /* Clip background to text shape */
        -webkit-text-fill-color: transparent;  /* Make text transparent to show gradient */
        text-align: center;  /* Center the title */
        padding: 1rem 0;  /* Add space above and below */
    }
    .sub-header {  /* Style for the smaller subtitle */
        text-align: center;  /* Center the subtitle */
        color: #666;  /* Set color to medium gray */
        font-size: 1.2rem;  /* Set font size */
        margin-bottom: 2rem;  /* Add space below */
    }
    .info-box {  /* Style for info messages */
        padding: 1rem;  /* Add padding inside */
        border-radius: 0.5rem;  /* Round the corners */
        background-color: #f0f2f6;  /* Light gray-blue background */
        border-left: 4px solid #667eea;  /* Blue stripe on the left */
        margin: 1rem 0;  /* Add vertical margin */
    }
    .success-box {  /* Style for success messages */
        padding: 1rem;  /* Add padding inside */
        border-radius: 0.5rem;  /* Round the corners */
        background-color: #d4edda;  /* Light green background */
        border-left: 4px solid #28a745;  /* Green stripe on the left */
        margin: 1rem 0;  /* Add vertical margin */
    }
    .stButton>button {  /* Style for all buttons */
        width: 100%;  /* Make buttons full width */
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);  /* Purple gradient background */
        color: white;  /* White text color */
        border: none;  /* Remove default border */
        padding: 0.75rem;  /* Add padding inside */
        font-size: 1rem;  /* Set font size */
        font-weight: bold;  /* Make text bold */
        border-radius: 0.5rem;  /* Round the corners */
    }
    .stButton>button:hover {  /* Style when mouse hovers over button */
        opacity: 0.9;  /* Make slightly transparent */
    }
    </style>
""", unsafe_allow_html=True)  # Allow HTML/CSS injection into Streamlit


def check_server_health():  # Define function to check if backend is alive
    """Check if backend server is running"""
    try:  # Start error handling block
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)  # Try to GET health status from backend
        return response.status_code == 200, response.json()  # Return True if status is 200, plus the data
    except:  # If connection fails
        return False, None  # Return False and no data


def upload_document(file, rebuild_index=False):  # Define function to send file to backend
    """Upload document to backend"""
    try:  # Start error handling block
        files = {"file": (file.name, file, file.type)}  # Prepare the file for uploading
        data = {"rebuild_index": rebuild_index}  # Prepare options (like clearing old docs)
        
        response = requests.post(  # Send the file using POST request
            f"{API_BASE_URL}/upload",  # The target upload endpoint
            files=files,  # Pass the file data
            data=data,  # Pass the options
            timeout=300  # Allow 5 minutes before giving up
        )
        
        if response.status_code == 200:  # If upload was successful
            return True, response.json()  # Return True and the result data
        else:  # If server returned an error
            return False, {"error": response.text}  # Return False and the error text
    except Exception as e:  # If something else went wrong
        return False, {"error": str(e)}  # Return False and the exception message


def ask_question_text(question, use_retrieval=True):  # Define function to ask tutor via text
    """Ask question via text"""
    try:  # Start error handling block
        data = {  # Prepare the question data as a dictionary
            "text": question,  # The actual question text
            "use_retrieval": use_retrieval,  # Whether to look in uploaded documents
            "return_audio": True  # Ask for a voice response as well
        }
        
        response = requests.post(  # Send the question to the backend
            f"{API_BASE_URL}/ask",  # The target "ask" endpoint
            data=data,  # Pass the dictionary data
            timeout=120  # Allow 2 minutes for a response
        )
        
        if response.status_code == 200:  # If request succeeded
            return True, response.json()  # Return True and the answer data
        else:  # If server failed
            return False, {"error": response.text}  # Return False and error message
    except Exception as e:  # If connection or other error occurs
        return False, {"error": str(e)}  # Return False and the error


def ask_question_audio(audio_bytes, use_retrieval=True):  # Define function to ask tutor via voice
    """Ask question via audio"""
    try:  # Start error handling block
        # Save audio temporarily
        audio_file = ("audio.wav", audio_bytes, "audio/wav")  # Package the audio bytes as a file
        
        files = {"audio": audio_file}  # Prepare files for the request
        data = {  # Prepare options
            "use_retrieval": use_retrieval,  # Use documents for context?
            "return_audio": True  # Should tutor speak back?
        }
        
        response = requests.post(  # Send voice to backend
            f"{API_BASE_URL}/ask",  # The target "ask" endpoint
            files=files,  # Pass the audio file
            data=data,  # Pass the options
            timeout=120  # Allow 2 minutes
        )
        
        if response.status_code == 200:  # If voice was processed successfully
            return True, response.json()  # Return True and the answer analysis
        else:  # If backend had trouble
            return False, {"error": response.text}  # Return False and error
    except Exception as e:  # Catch any programming errors
        return False, {"error": str(e)}  # Return False and error details


def get_audio_file(filename):  # Define function to download audio from server
    """Get audio file from backend"""
    try:  # Error handling
        response = requests.get(f"{API_BASE_URL}/audio/{filename}", timeout=30)  # GET the audio file bytes
        if response.status_code == 200:  # If file exists and is retrieved
            return response.content  # Return the raw audio bytes
        return None  # Return nothing if status code is not 200
    except:  # If server is unreachable
        return None  # Return nothing


def main():  # Define the main application logic
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🎓 EchoLearn AI</h1>', unsafe_allow_html=True)  # Draw the main title
    st.markdown(  # Draw the subtitle
        '<p class="sub-header">Your Personal Voice Tutor - Learn from Your Documents</p>',
        unsafe_allow_html=True
    )
    
    # Check server health
    is_healthy, health_data = check_server_health()  # Check if backend is running
    
    if not is_healthy:  # If backend is not connected
        st.error("⚠️ Backend server is not running. Please start the server with: `python server.py`")  # Show error
        st.stop()  # Stop the Streamlit app here
    
    # Sidebar
    with st.sidebar:  # Everything inside this block goes into the sidebar
        st.header("📚 Document Upload")  # Set sidebar header
        
        # File uploader
        uploaded_file = st.file_uploader(  # Show the file upload UI
            "Upload PDF or Jupyter Notebook",  # Instruction text
            type=["pdf", "ipynb"],  # Allowed file extensions
            help="Upload learning materials to ask questions about"  # Tooltip text
        )
        
        rebuild_index = st.checkbox(  # Show checkbox to reset documents
            "Rebuild index (clear previous documents)",  # Label
            help="Check this to replace all previous documents"  # Tooltip
        )
        
        if uploaded_file is not None:  # If a file was selected
            # Check if this is a new file or we need to re-process
            file_key = f"processed_{uploaded_file.name}_{uploaded_file.size}"  # Create unique key for this file
            if st.session_state.get("last_uploaded_file") != file_key:  # If file is different from last time
                with st.spinner("Analyzing document..."):  # Show a loading animation
                    success, result = upload_document(uploaded_file, rebuild_index)  # Send file to backend
                    
                    if success:  # If upload worked
                        st.session_state["last_uploaded_file"] = file_key  # Save file key in session
                        st.session_state["upload_success"] = result  # Save result in session
                        st.rerun()  # Refresh the page to show new state
                    else:  # If upload failed
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")  # Show error message
        
        # Display success message and audio if just uploaded
        if st.session_state.get("upload_success"):  # If we have a successful upload in memory
            result = st.session_state["upload_success"]  # Get the results
            st.success("✅ Your PDF is successfully uploaded. Now ask me a question.")  # Show success banner
            
            # Autoplay greeting if provided
            if result.get("greeting_audio"):  # If backend sent a greeting voice
                audio_filename = Path(result["greeting_audio"]).name  # Get the audio filename
                audio_data = get_audio_file(audio_filename)  # Download the audio bytes
                if audio_data:  # If bytes were received
                    st.audio(audio_data, format="audio/mp3")  # Play the audio greeting
            
            with st.expander("📄 Document Details"):  # Create a collapsible detail section
                st.json({  # Display details as formatted JSON
                    "Filename": result["filename"],  # Show name of file
                    "Chunks Created": result["num_chunks"],  # Show number of text pieces
                    "Processing Time": f"{result['processing_time']}s"  # Show how long it took
                })
        
        st.divider()  # Draw a horizontal line
        
        # System status
        st.header("🔧 System Status")  # Sidebar section for stats
        
        if health_data:  # If we have server health info
            stats = health_data.get("vector_db_stats", {})  # Get database statistics
            
            st.metric("Documents in Index", stats.get("num_documents", 0))  # Show count of files indexed
            
            if stats.get("num_documents", 0) > 0:  # If documents are available
                st.success("✅ Ready to answer questions")  # Show green "ready" message
            else:  # If index is empty
                st.info("ℹ️ Upload documents to get started")  # Show "get started" tip
        
        st.divider()  # Another separator line
        
        # Clear memory button
        if st.button("🗑️ Clear Conversation"):  # If user clicks clear button
            try:  # Try to contact server
                requests.post(f"{API_BASE_URL}/clear-memory")  # Tell backend to forget chat history
                st.success("Conversation cleared!")  # Show success message
                st.rerun()  # Refresh the UI
            except:  # If request fails
                st.error("Failed to clear conversation")  # Show error
    
    # Main content area
    st.header("💬 Ask Your Tutor")  # Section title for asking questions
    
    # Tabs for different input methods
    tab1, tab2 = st.tabs(["🎤 Voice Input", "⌨️ Text Input"])  # Create two tabs for Voice and Text
    
    with tab1:  # Content for the Voice Input tab
        st.info("🎤 Click the microphone button to record your question")  # Instruction banner
        
        # Audio recorder
        audio_bytes = audio_recorder(  # Show the voice recorder widget
            text="Click to record",  # Label on recorder
            recording_color="#e74c3c",  # Color when recording (red)
            neutral_color="#667eea",  # Color when idle (blue)
            icon_size="3x",  # Size of the icon
            pause_threshold=Config.STT_PAUSE_THRESHOLD,  # How long to wait for silence
            energy_threshold=Config.STT_ENERGY_THRESHOLD  # Loudness threshold for recording
        )
        
        use_retrieval_voice = st.checkbox(  # Option to use uploaded docs for voice question
            "Use document context",  # Label
            value=True,  # Default to ON
            key="use_retrieval_voice"  # Unique key for this widget
        )
        
        if audio_bytes:  # If user finished recording
            with st.spinner("Processing your question..."):  # Show loading spinner
                # Send audio to backend
                success, result = ask_question_audio(audio_bytes, use_retrieval_voice)  # Process voice
                
                if success:  # If backend understood and answered
                    # Display question
                    st.markdown("### Your Question:")  # Section for question text
                    st.info(result["question"])  # Show transcribed question
                    
                    # Display answer
                    st.markdown("### Tutor's Answer:")  # Section for tutor answer
                    st.success(result["answer"])  # Show answer text
                    
                    # Play audio response
                    if result.get("audio_path"):  # If a voice response file was made
                        audio_filename = Path(result["audio_path"]).name  # Get the filename
                        audio_data = get_audio_file(audio_filename)  # Download the audio
                        
                        if audio_data:  # If download worked
                            st.audio(audio_data, format="audio/mp3")  # Play the tutor's voice
                    
                    # Show sources if used
                    if result.get("sources") and len(result["sources"]) > 0:  # If answer came from docs
                        with st.expander(f"📖 Sources ({len(result['sources'])} documents)"):  # Openable source list
                            for i, source in enumerate(result["sources"], 1):  # Loop through sources
                                st.markdown(f"**Source {i}** (Score: {source['score']:.3f})")  # Show relevance score
                                st.text(source["text"][:300] + "...")  # Show first 300 characters of source
                                st.divider()  # Add line between sources
                    
                    # Show timing
                    with st.expander("⏱️ Performance Metrics"):  # Section for speed info
                        st.json(result["timing"])  # Display how fast processing was
                else:  # If voice processing failed
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")  # Display error
    
    with tab2:  # Content for the Text Input tab
        st.info("⌨️ Type your question below")  # Instruction for text
        
        # Text input
        question_text = st.text_area(  # Multi-line text box
            "Your Question:",  # Title
            placeholder="e.g., What is machine learning?",  # Help text inside box
            height=100  # Size of text box
        )
        
        col1, col2 = st.columns([3, 1])  # Create two columns (wider left, narrower right)
        
        with col1:  # Left column
            use_retrieval_text = st.checkbox(  # Opt-in to use documents context
                "Use document context",  # Checkbox label
                value=True,  # Default to Checked
                key="use_retrieval_text"  # Unique key for widget
            )
        
        with col2:  # Right column
            ask_button = st.button("🚀 Ask", use_container_width=True)  # Button to submit question
        
        if ask_button and question_text.strip():  # if button clicked and box is not empty
            with st.spinner("Thinking..."):  # Show thinking spinner
                success, result = ask_question_text(question_text, use_retrieval_text)  # Call API
                
                if success:  # If successful
                    # Display answer
                    st.markdown("### Tutor's Answer:")  # Heading
                    st.success(result["answer"])  # Show answer in green box
                    
                    # Play audio response
                    if result.get("audio_path"):  # If tutor voice is available
                        st.markdown("### 🔊 Listen to the answer:")  # Voice heading
                        audio_filename = Path(result["audio_path"]).name  # Filename
                        audio_data = get_audio_file(audio_filename)  # Download
                        
                        if audio_data:  # If download OK
                            st.audio(audio_data, format="audio/mp3")  # Play audio
                    
                    # Show sources if used
                    if result.get("sources") and len(result["sources"]) > 0:  # If results from docs
                        with st.expander(f"📖 Sources ({len(result['sources'])} documents)"):  # Openable list
                            for i, source in enumerate(result["sources"], 1):  # Loop sources
                                st.markdown(f"**Source {i}** (Score: {source['score']:.3f})")  # Score
                                st.text(source["text"][:300] + "...")  # Snippet
                                st.divider()  # Divider
                    
                    # Show timing
                    with st.expander("⏱️ Performance Metrics"):  # Metrics section
                        st.json(result["timing"])  # Show timings
                else:  # On error
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")  # Show error
        
        elif ask_button:  # If button clicked but box is empty
            st.warning("⚠️ Please enter a question")  # Warning message
    
    # Footer
    st.divider()  # Full-width line
    st.markdown(  # Centered footer text
        "<p style='text-align: center; color: #666;'>Built with ❤️ using RAG, LangChain, and FastAPI</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":  # If script is run directly
    main()  # Start the application
