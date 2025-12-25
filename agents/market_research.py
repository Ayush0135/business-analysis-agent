from utils.llm import call_llm
from utils.search import get_search_summary

def run(business_idea, industry, region="Global"):
    print(f"--- Market Research Agent Running for {business_idea} ---")
    
    # 1. Gather Data
    queries = [
        f"market size {industry} {region} 2024 2025",
        f"{industry} trends {region}",
        f"TAM SAM SOM {business_idea} {industry}",
        f"growth rate {industry} {region}"
    ]
    
    search_data = ""
    for q in queries:
        print(f"Searching: {q}...")
        search_data += get_search_summary(q)
    
    # 2. Analyze
    prompt = f"""
    You are a Market Research Expert.
    Analyze the market for the following business idea:
    Idea: {business_idea}
    Industry: {industry}
    Region: {region}
    
    Use the search data below to provide a report covering:
    1. Market Size (TAM, SAM, SOM) with numbers if possible.
    2. Industry Trends.
    3. Growth Rate (CAGR).
    4. Demand Signals.
    
    Search Data:
    {search_data}
    
    Output strictly in Markdown format.
    """
    
    return call_llm(prompt)
