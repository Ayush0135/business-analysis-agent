from utils.llm import call_llm

def run(business_idea, market_report, competitor_report, customer_report):
    print(f"--- SWOT Analysis Agent Running ---")
    
    prompt = f"""
    You are a Strategic Analyst.
    Perform a SWOT analysis for the business idea: {business_idea}
    
    Base your analysis on the following reports:
    
    --- Market Research ---
    {market_report}
    
    --- Competitor Analysis ---
    {competitor_report}
    
    --- Customer Insights ---
    {customer_report}
    
    Output a detailed SWOT Matrix (Strengths, Weaknesses, Opportunities, Threats).
    Also provide 3 Strategic Implications based on the SWOT.
    
    Output strictly in Markdown format.
    """
    
    return call_llm(prompt)
