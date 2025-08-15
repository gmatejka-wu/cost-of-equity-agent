import requests

def run(inputs, context):
    ticker = inputs.get("ticker")
    country = inputs.get("country")
    industry = inputs.get("industry")

    url = "https://api.marktrendite.ai/CostofEquity"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "ticker": ticker,
        "country": country,
        "industry": industry
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        cost_of_equity = data.get("cost_of_equity")
        return {
            "result": f"The cost of equity for {ticker} is {cost_of_equity}."
        }
    else:
        return {
            "result": f"Error: {response.status_code} - {response.text}"
        }
