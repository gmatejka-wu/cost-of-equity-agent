def run(inputs, context):
    isin = inputs.get("isin", "")
    
    # Test with mock data to verify deployment works
    if isin:
        return {"result": f"Test successful for ISIN: {isin}"}
    else:
        return {"result": "Test deployment successful - agent is working"}
