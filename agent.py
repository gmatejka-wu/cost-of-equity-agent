import requests

def run(inputs, context):
    isin = inputs.get("isin", "").upper()
    
    try:
        # Add timeout to prevent hanging
        response = requests.get(
            "https://api.marktrendite.ai/CostofEquity", 
            timeout=10
        )
        
        if response.status_code != 200:
            return {"result": f"API returned status {response.status_code}"}
        
        data = response.json()
        
        if not data:
            return {"result": "API returned empty data"}
        
        if isin:
            for company in data:
                if company.get("isin") == isin:
                    return {"result": f"{isin}: {company.get('gewichtet_3')}%"}
            return {"result": f"{isin} not found"}
        else:
            return {"result": f"Retrieved {len(data)} companies"}
            
    except requests.exceptions.Timeout:
        return {"result": "API timeout - try again later"}
    except requests.exceptions.RequestException as e:
        return {"result": f"Network error: {type(e).__name__}"}
    except Exception as e:
        return {"result": f"Error: {type(e).__name__}"}
