from utils.llm import call_llm
from utils.search import get_search_summary

def run(business_idea, industry, region):
    print(f"--- Financial Estimation Agent Running ---")
    
    queries = [
        f"startup costs for {industry} business in {region}",
        f"average pricing {industry} services products",
        f"operating margins {industry}"
    ]
    
    search_data = ""
    for q in queries:
        print(f"Searching: {q}...")
        search_data += get_search_summary(q)
        
    prompt = f"""
    You are a Financial Analyst for Startups.
    Estimate the financials for: {business_idea}
    
    Search Data:
    {search_data}
    
    Provide a REALISTIC estimation (not hallucinated, use ranges if unsure):
    1. Capital Expenditure (CAPEX) - Setup costs.
    2. Operating Expenditure (OPEX) - Monthly running costs.
    3. Pricing Strategy suggestion.
    4. Revenue Projections (Year 1, Year 2, Year 3).
    5. Break-even analysis rough estimate.
    
    Output strictly in Markdown format.
    """
    
    return call_llm(prompt)
