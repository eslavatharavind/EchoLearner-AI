"""
System Check Script for EchoLearn AI - This file checks if your computer is ready
Verifies all components are properly installed and configured - To prevent math/code errors
"""

import sys  # Import sys to check things about the Python language itself
from pathlib import Path  # Import Path for checking for local files and folders

def print_header(text):  # Helper function to print a pretty title in the console
    """Print formatted header"""
    print("\n" + "=" * 60)  # Print a line of 60 characters
    print(f"  {text}")  # Print the title text
    print("=" * 60)  # Print another line

def check_python_version():  # Function to see if your Python is new enough
    """Check Python version"""
    print_header("Checking Python Version")  # Print section title
    version = sys.version_info  # Get the version numbers
    print(f"Python {version.major}.{version.minor}.{version.micro}")  # Show the version found
    
    if version.major >= 3 and version.minor >= 9:  # We need at least 3.9
        print("✅ Python version is compatible")  # Good news
        return True
    else:
        print("❌ Python 3.9+ required")  # Bad news
        return False

def check_dependencies():  # Function to see if you installed all the "apps" needed
    """Check if all required packages are installed"""
    print_header("Checking Dependencies")  # Print section title
    
    # List of all the libraries we need to make EchoLearn work
    required_packages = [
        "fastapi", "uvicorn", "streamlit", "langchain",
        "faiss", "sentence_transformers", "faster_whisper",
        "openai", "PyMuPDF", "nbformat", "pydantic"
    ]
    
    missing = []  # List for any packages not found
    
    for package in required_packages:  # Loop through each one
        try:
            # Try to "load" the package to see if it's installed
            __import__(package if package != "PyMuPDF" else "fitz")
            print(f"✅ {package}")  # Good news
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")  # Missing!
            missing.append(package)  # Remember this missing one
    
    if missing:  # If we missed anything
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")  # Tell user how to fix
        return False
    else:
        print("\n✅ All dependencies installed")
        return True

def check_configuration():  # Function to check your secret API key settings
    """Check configuration files"""
    print_header("Checking Configuration")
    
    # Check if the secret .env file is there
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file exists")
        
        # Try to load the code that reads the .env file
        try:
            from config import Config
            print("✅ Configuration loaded successfully")
            
            # Make sure all the folders (data, logs, etc.) are present
            Config.ensure_directories()
            print("✅ Data directories created")
            
            # Check if API keys are filled in
            try:
                Config.validate_config()  # Run the validation function
                print("✅ Configuration is valid")
                return True
            except ValueError as e:
                # API keys are missing, but the file exists, so we just warn
                print(f"⚠️  Configuration warning: {e}")
                print("   You'll need to add API keys before running")
                return True
                
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return False
    else:
        print("❌ .env file not found")
        print("   Create .env from .env.example and add your API keys")
        return False

def check_file_structure():  # Function to check if you have all the source code files
    """Check if all required files exist"""
    print_header("Checking File Structure")
    
    # List of all the .py files we wrote for this project
    required_files = [
        "config.py", "server.py", "app.py",
        "pdf_loader.py", "notebook_loader.py", "text_cleaner.py",
        "chunker.py", "build_vector_db.py",
        "retriever.py", "prompt.py", "tutor_agent.py", "memory.py",
        "speech_to_text.py", "text_to_speech.py",
        "requirements.txt", ".env.example", "README.md"
    ]
    
    missing = []  # List for missing files
    
    for file in required_files:  # Check each file name
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NOT FOUND")
            missing.append(file)
    
    if missing:  # If anything is missing
        print(f"\n⚠️  Missing files: {', '.join(missing)}")
        return False
    else:
        print("\n✅ All required files present")
        return True

def test_imports():  # Function to make sure our code files can "talk" to each other
    """Test importing key modules"""
    print_header("Testing Module Imports")
    
    # List of (file_name, important_tool_name)
    modules = [
        ("config", "Config"),
        ("pdf_loader", "PDFLoader"),
        ("notebook_loader", "NotebookLoader"),
        ("text_cleaner", "TextCleaner"),
        ("chunker", "TextChunker"),
        ("build_vector_db", "VectorDBBuilder"),
        ("retriever", "DocumentRetriever"),
        ("prompt", "TutorPrompts"),
        ("memory", "ConversationMemory"),
        ("speech_to_text", "SpeechToText"),
        ("text_to_speech", "TextToSpeech"),
        ("tutor_agent", "TutorAgent"),
    ]
    
    success = True  # Track if all worked
    
    for module_name, class_name in modules:  # Try loading each pair
        try:
            module = __import__(module_name)
            getattr(module, class_name)  # See if the class exists inside the file
            print(f"✅ {module_name}.{class_name}")
        except Exception as e:
            print(f"❌ {module_name}.{class_name} - Error: {e}")
            success = False
    
    if success:
        print("\n✅ All modules import successfully")
    else:
        print("\n⚠️  Some modules failed to import")
    
    return success

def test_basic_functionality():  # Function to do a small test run of the cleanup/search code
    """Test basic functionality of key components"""
    print_header("Testing Basic Functionality")
    
    try:
        # Test 1: Can we clean messy text?
        from text_cleaner import TextCleaner
        cleaner = TextCleaner()
        result = cleaner.clean("Test   text    with    spaces")
        assert "Test text with spaces" in result
        print("✅ TextCleaner works")
        
        # Test 2: Can we split long text into pieces?
        from chunker import TextChunker
        chunker = TextChunker()
        chunks = chunker.chunk("This is a test. " * 100)
        assert len(chunks) > 0
        print("✅ TextChunker works")
        
        # Test 3: Can we load our teaching scripts?
        from prompt import TutorPrompts
        prompt = TutorPrompts.get_system_prompt()
        assert len(prompt) > 0
        print("✅ TutorPrompts works")
        
        # Test 4: Can we remember a simple chat fact?
        from memory import ConversationMemory
        memory = ConversationMemory()
        memory.add_interaction("Question?", "Answer!")
        assert len(memory.get_history()) == 1
        print("✅ ConversationMemory works")
        
        print("\n✅ Basic functionality tests passed")
        return True
        
    except Exception as e:
        print(f"\n❌ Functionality test failed: {e}")
        return False

def print_summary(checks):  # Function to show a final report card
    """Print summary of all checks"""
    print_header("System Check Summary")
    
    total = len(checks)  # Total number of tests
    passed = sum(checks.values())  # Number of PASS results
    
    for check_name, result in checks.items():  # List each check and its grade
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:  # If 100% score
        print("\n🎉 System is ready to use!")
        print("\nNext steps:")
        print("1. Add your API keys to .env file")
        print("2. Run: python server.py")
        print("3. Run: streamlit run app.py (in new terminal)")
    else:
        print("\n⚠️  Please fix the issues above before running the system")

def main():  # High-level control function
    """Run all checks"""
    print("=" * 60)
    print("  EchoLearn AI - System Check")
    print("=" * 60)
    
    checks = {}  # Store results here
    
    # Run each check one by one
    checks["Python Version"] = check_python_version()
    checks["File Structure"] = check_file_structure()
    checks["Dependencies"] = check_dependencies()
    checks["Configuration"] = check_configuration()
    checks["Module Imports"] = test_imports()
    checks["Basic Functionality"] = test_basic_functionality()
    
    # Print the final report card
    print_summary(checks)

if __name__ == "__main__":  # This runs as soon as you type 'python check_system.py'
    main()
