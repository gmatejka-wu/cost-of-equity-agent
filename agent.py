import requests

def run(inputs, context):
    # The API doesn't actually use input parameters - it returns all companies
    isin_filter = inputs.get("isin", "").upper() if inputs.get("isin") else None
    
    url = "https://api.marktrendite.ai/CostofEquity"
    
    try:
        # The API works with GET request, not POST
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                # If ISIN is provided, try to find that specific company
                if isin_filter:
                    for company in data:
                        if company.get("isin") == isin_filter:
                            cost_of_equity = company.get("gewichtet_3")
                            ddm_cost = company.get("ddm_3")
                            rim_cost = company.get("rim_3")
                            market_value = company.get("MV")
                            date = company.get("date")
                            
                            return {
                                "result": f"Cost of equity for ISIN {isin_filter}: Weighted: {cost_of_equity}%, DDM: {ddm_cost}%, RIM: {rim_cost}%. Market Value: {market_value}M. Date: {date}"
                            }
                    
                    return {
                        "result": f"ISIN {isin_filter} not found in the database. Available companies: {len(data)}"
                    }
                else:
                    # No ISIN provided, return summary info
                    total_companies = len(data)
                    avg_cost = sum(company.get("gewichtet_3", 0) for company in data) / total_companies
                    latest_date = data[0].get("date") if data else "Unknown"
                    
                    # Show a few examples
                    examples = []
                    for i, company in enumerate(data[:3]):
                        isin = company.get("isin")
                        cost = company.get("gewichtet_3")
                        examples.append(f"{isin}: {cost}%")
                    
                    return {
                        "result": f"Retrieved {total_companies} companies (Date: {latest_date}). Average weighted cost of equity: {avg_cost:.2f}%. Examples: {', '.join(examples)}. Provide an ISIN code to get specific company data."
                    }
            else:
                return {
                    "result": "API returned empty data or unexpected format."
                }
        else:
            return {
                "result": f"Error: API returned status code {response.status_code} - {response.text}"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "result": f"Network error: {str(e)}"
        }
    except Exception as e:
        return {
            "result": f"Unexpected error: {str(e)}"
        }
