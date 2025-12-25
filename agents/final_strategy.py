from utils.llm import call_llm

def run(business_idea, market_res, comp_analysis, cust_insights, swot_analysis, financial_est, risk_assess):
    print(f"--- FInal Strategy Agent Running ---")
    
    prompt = f"""
    You are the Chief Strategy Officer.
    Synthesize all the following reports into a Final Strategy Report for the business idea: {business_idea}
    
    --- Market Research ---
    {market_res}
    
    --- Competitor Analysis ---
    {comp_analysis}
    
    --- Customer Insights ---
    {cust_insights}
    
    --- SWOT Analysis ---
    {swot_analysis}
    
    --- Financial Estimation ---
    {financial_est}
    
    --- Risk & Feasibility ---
    {risk_assess}
    
    Your Task:
    1. Provide a "Verdict": Go or No-Go?
    2. Outline a clear Entry Strategy.
    3. Define Positioning Strategy.
    4. Create a 30-60-90 Day Action Plan.
    5. Summarize the biggest opportunity and the biggest threat.
    
    Output strictly in Markdown format.
    """
    
    return call_llm(prompt)
