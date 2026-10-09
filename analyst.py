import yfinance as yf
from ddgs import DDGS

def get_stock_data(ticker: str) -> dict:
    """Fetches key stock data for a given ticker."""
    try:
        t = yf.Ticker(ticker)
        info = t.info
        fast_info = t.fast_info
        
        # Check if the ticker is valid (yfinance returns empty/bare info for invalid ones)
        if not info or 'shortName' not in info:
            return {"error": f"Ticker '{ticker}' not found or has no data."}
            
        current_price = fast_info.get('lastPrice', info.get('currentPrice'))
        prev_close = fast_info.get('previousClose', info.get('previousClose'))
        
        day_change_pct = None
        if current_price and prev_close:
            day_change_pct = ((current_price - prev_close) / prev_close) * 100
            
        return {
            "company_name": info.get('shortName', ticker),
            "current_price": current_price,
            "previous_close": prev_close,
            "day_change_percent": round(day_change_pct, 2) if day_change_pct is not None else None,
            "market_cap": fast_info.get('marketCap', info.get('marketCap')),
            "pe_ratio": info.get('trailingPE', info.get('forwardPE')),
            "52_week_high": fast_info.get('yearHigh', info.get('fiftyTwoWeekHigh')),
            "52_week_low": fast_info.get('yearLow', info.get('fiftyTwoWeekLow')),
        }
    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker}: {str(e)}"}

def get_news(ticker: str) -> list:
    """Fetches recent news headlines for a given ticker."""
    try:
        with DDGS() as ddgs:
            # Search for recent news related to the ticker
            results = ddgs.news(f"{ticker} stock", max_results=5)
            if not results:
                return [{"error": f"No news found for {ticker}."}]
                
            news_list = []
            for r in results:
                news_list.append({
                    "title": r.get('title'),
                    "source": r.get('source'),
                    "link": r.get('url'),
                    "snippet": r.get('body')
                })
            return news_list
    except Exception as e:
        return [{"error": f"Failed to fetch news for {ticker}: {str(e)}"}]

if __name__ == "__main__":
    import json
    
    print("Testing get_stock_data('AAPL'):")
    print(json.dumps(get_stock_data("AAPL"), indent=2))
    
    print("\nTesting get_stock_data('TSLA'):")
    print(json.dumps(get_stock_data("TSLA"), indent=2))
    
    print("\nTesting get_stock_data('FAKE_TICKER'):")
    print(json.dumps(get_stock_data("FAKE_TICKER"), indent=2))
    
    print("\nTesting get_news('AAPL'):")
    print(json.dumps(get_news("AAPL"), indent=2))
