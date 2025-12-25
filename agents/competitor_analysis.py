from utils.llm import call_llm
from utils.search import get_search_summary

def run(business_idea, industry):
    print(f"--- Competitor Analysis Agent Running ---")
    
    queries = [
        f"top competitors for {business_idea}",
        f"{industry} companies pricing models",
        f"alternatives to {business_idea}"
    ]
    
    search_data = ""
    for q in queries:
        print(f"Searching: {q}...")
        search_data += get_search_summary(q)
        
    prompt = f"""
    You are a Competitor Analysis Expert.
    Identify competitors for this business idea: {business_idea}
    
    Use the search data provided.
    
    Output a report covering:
    1. Direct & Indirect Competitors (List top 3-5).
    2. Competitor Pricing Models (if available).
    3. Their Value Propositions.
    4. Market Gaps (Blue Ocean vs Red Ocean).
    
    Search Data:
    {search_data}
    
    Output strictly in Markdown format.
    """
    
    return call_llm(prompt)
