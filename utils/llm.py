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
    Calls various LLMs with a robust fallback mechanism & retries.
    Order: Groq -> Gemini
    """
    context = ""
    if system_instruction:
        context = f"System Instruction: {system_instruction}\n\n"
    
    full_prompt = context + prompt

    def attempt_groq():
        if not GROQ_API_KEY: return None
        # Set a 8-second timeout to ensure we fail over quickly if it hangs
        client = Groq(api_key=GROQ_API_KEY, timeout=8.0)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": full_prompt}],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content

    def attempt_gemini():
        if not GEMINI_API_KEY: return None
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash-exp') 
        # Gemini doesn't have a simple timeout param in generate_content, but it's usually fast
        response = model.generate_content(full_prompt)
        return response.text

    # 1. FAST Try Groq (Max 1 Retry with short sleep)
    # We prioritize switching over retrying endlessly
    for i in range(2): 
        try:
            res = attempt_groq()
            if res: return res
        except Exception as e:
            print(f"⚠️ Groq Attempt {i+1} Failed: {e}")
            if i == 0: time.sleep(0.5) # Short pause before 1 single retry

    print("🔻 Groq unavailable. Switching to Gemini immediately...")

    # 2. Fallback to Gemini (Reliability Focus)
    for i in range(2):
        try:
            res = attempt_gemini()
            if res: return res
        except Exception as e:
            print(f"⚠️ Gemini Attempt {i+1} Failed: {e}")
            time.sleep(1)

    return "❌ **System Error**: All AI agents are currently unavailable. Please check your API keys or try again later."
