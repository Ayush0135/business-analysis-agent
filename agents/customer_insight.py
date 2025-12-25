from utils.llm import call_llm
from utils.search import get_search_summary

def run(business_idea, industry):
    print(f"--- Customer Insight Agent Running ---")
    
    # Search for pain points might be useful
    queries = [
        f"customer complaints {industry}",
        f"what customers want in {industry}",
        f"user problems with {business_idea} alternatives"
    ]
    
    search_data = ""
    for q in queries:
        print(f"Searching: {q}...")
        search_data += get_search_summary(q)

    prompt = f"""
    You are a Consumer Psychology Expert.
    Define the target audience and their needs for: {business_idea}
    
    Search Data Context:
    {search_data}
    
    Output a report covering:
    1. Target Audience Personas (Create 2-3 detailed personas).
    2. Key Pain Points they face.
    3. Willingness to Pay drivers.
    4. Behavior Patterns.
    
    Output strictly in Markdown format.
    """
    
    return call_llm(prompt)
