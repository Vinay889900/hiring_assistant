import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in environment.")
else:
    print(f"✅ API Key found (starts with: {api_key[:4]}...)")
    # Wrap the whole block in try/except 
    try:
        with open("model_list.txt", "w", encoding="utf-8") as f:
            genai.configure(api_key=api_key)
            f.write(f"Library version: {genai.__version__}\n")
            
            f.write("\nListing available models...\n")
            try:
                models = list(genai.list_models())
                if not models:
                    f.write("⚠️ No models found. Check API key permissions.\n")
                for m in models:
                    f.write(f"- Name: {m.name}\n")
                    f.write(f"  Supported methods: {m.supported_generation_methods}\n")
            except Exception as list_err:
                f.write(f"Error calling list_models: {list_err}\n")
            
    except Exception as e:
        with open("model_list.txt", "w", encoding="utf-8") as f:
            f.write(f"❌ Error listing models: {e}\n")
