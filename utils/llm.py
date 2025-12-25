import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq
import cohere
from huggingface_hub import InferenceClient

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

def call_llm(prompt, system_instruction=None, model_type="groq"):
    """
    Calls various LLMs with a robust fallback mechanism.
    Order: Groq -> Gemini -> Cohere -> Hugging Face
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

    # 3. Fallback to Cohere
    if COHERE_API_KEY:
        try:
            co = cohere.Client(COHERE_API_KEY)
            response = co.chat(
                message=full_prompt,
                model="command-r-plus" 
            )
            return response.text
        except Exception as e:
            print(f"⚠️ Cohere Failed: {e}")

    # 4. Fallback to Hugging Face
    if HF_TOKEN:
        try:
            client = InferenceClient(token=HF_TOKEN)
            # using Mistral 7B as a reliable general model
            response = client.text_generation(
                full_prompt, 
                model="mistralai/Mistral-7B-Instruct-v0.3", 
                max_new_tokens=2000
            )
            return response
        except Exception as e:
            print(f"⚠️ Hugging Face Failed: {e}")

    return "❌ Error: All LLM attempts failed. Please check your API keys."
