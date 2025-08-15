import requests

def run(inputs, context):
    isin = inputs.get("isin", "").upper()
    
    try:
        response = requests.get("https://api.marktrendite.ai/CostofEquity")
        
        if response.status_code != 200:
            return {"result": f"API Error: {response.status_code}"}
        
        data = response.json()
        
        if isin:
            # Find specific company
            for company in data:
                if company.get("isin") == isin:
                    cost = company.get("gewichtet_3")
                    return {"result": f"Cost of equity for {isin}: {cost}%"}
            return {"result": f"ISIN {isin} not found"}
        else:
            # Return summary
            total = len(data)
            avg_cost = sum(c.get("gewichtet_3", 0) for c in data) / total
            return {"result": f"Found {total} companies. Average cost of equity: {avg_cost:.2f}%"}
            
    except Exception as e:
        return {"result": f"Error: {str(e)}"}
