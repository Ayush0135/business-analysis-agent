import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq
# import cohere  <-- Commented out to save space
# from huggingface_hub import InferenceClient <-- Commented out to save space

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# COHERE_API_KEY = os.getenv("COHERE_API_KEY")
# HF_TOKEN = os.getenv("HF_TOKEN")

def call_llm(prompt, system_instruction=None, model_type="groq"):
    """
    Calls various LLMs with a robust fallback mechanism.
    Order: Groq -> Gemini
    (Cohere and HF removed for Vercel size limits)
    """
    context = ""
    if system_instruction:
        context = f"System Instruction: {system_instruction}\n\n"
    
    full_prompt = context + prompt

    # 1. Try Groq (Fastest & Good Free Tier)
    if GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": full_prompt}],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Groq Failed: {e}")

    # 2. Fallback to Gemini
    if GEMINI_API_KEY:
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-2.0-flash-exp') 
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"⚠️ Gemini Failed: {e}")

    return "❌ Error: All LLM attempts failed. Please check your API keys."
