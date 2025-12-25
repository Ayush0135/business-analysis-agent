from utils.llm import call_llm
from utils.search import get_search_summary

def run(business_idea, industry, region):
    print(f"--- Risk & Feasibility Agent Running ---")
    
    queries = [
        f"legal requirements for {industry} in {region}",
        f"risks of starting {business_idea}",
        f"market saturation {industry}"
    ]
    
    search_data = ""
    for q in queries:
        print(f"Searching: {q}...")
        search_data += get_search_summary(q)
        
    prompt = f"""
    You are a Risk Management Consultant.
    Assess the risks for: {business_idea}
    
    Search Data:
    {search_data}
    
    Output a report covering:
    1. Potential Risks (Regulatory, Market, Operational).
    2. Risk Severity Score (High/Medium/Low) for each.
    3. Mitigation Strategies.
    4. Feasibility Score (0-10) with reasoning.
    
    Output strictly in Markdown format.
    """
    
    return call_llm(prompt)
