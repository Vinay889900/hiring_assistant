# API Key Configuration Instructions

## Important: OpenAI API Key Setup

This application requires a valid OpenAI API key to function properly. Please follow these steps:

### Option 1: Environment Variable (Recommended)
1. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="sk-your-actual-api-key-here"
   ```

2. Update the `chatbot_logic.py` file to use the environment variable:
   ```python
   client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
   ```

### Option 2: Direct API Key (Less Secure)
1. Replace the placeholder in `chatbot_logic.py`:
   ```python
   client = OpenAI(api_key="sk-your-actual-api-key-here")
   ```

### Getting an OpenAI API Key
1. Visit https://platform.openai.com/
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and use it in one of the methods above

### Security Note
Never commit your actual API key to version control. Always use environment variables or secure configuration files in production environments.

## Testing the Application
Once you have configured your API key, you can test the application by running:
```bash
streamlit run app.py
```

The application will start and be accessible at http://localhost:8501

