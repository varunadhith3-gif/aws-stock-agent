"""
Stock Market Research Agent
----------------------------
Uses the Strands Agents framework with Claude (via Amazon Bedrock) as the
LLM backbone.  Two tools are exposed to the agent:
  - get_stock_data : fetch live price / fundamentals via yfinance
  - get_news       : fetch recent headlines via DuckDuckGo
"""

from strands import Agent, tool
from analyst import get_stock_data, get_news


# ─── Tool definitions ────────────────────────────────────────────────────────
# The @tool decorator wraps our analyst functions so the agent can call them.

@tool
def stock_data(ticker: str) -> dict:
    """
    Fetch live stock price and key fundamentals for a given ticker symbol.

   Args:
        ticker: The stock ticker symbol (e.g. 'AAPL', 'TSLA', 'MSFT').

    Returns:
        A dictionary with current_price, market_cap, pe_ratio,
        52-week high/low, and day change percentage.
    """
    return get_stock_data(ticker)


@tool
def news(ticker: str) -> list:
    """
    Fetch the 5 most recent news headlines for a given stock ticker.

    Args:
        ticker: The stock ticker symbol (e.g. 'AAPL', 'TSLA', 'MSFT').

    Returns:
        A list of recent news items with title, source, link, and snippet.
    """
    return get_news(ticker)


# ─── Agent setup ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a professional stock market research assistant.
When a user asks about a stock, you MUST:
1. Call the stock_data tool to get the current price and fundamentals.
2. Call the news tool to fetch recent headlines.
3. Combine both to give a concise, well-structured analysis covering:
   - Current price and today's performance
   - Key fundamentals (market cap, P/E ratio, 52-week range)
   - Summary of recent news sentiment
   - A brief outlook based on the data
Always cite the data you retrieved and be clear about what is fact vs opinion."""

agent = Agent(
    model="amazon.nova-micro-v1:0",
    tools=[stock_data, news],
    system_prompt=SYSTEM_PROMPT,
)


# ─── Main loop ───────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Stock Market Research Agent  (type 'quit' to exit)")
    print("=" * 60)
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        print()
        response = agent(user_input)
        print(f"\nAgent: {response}\n")

if __name__ == "__main__":
    main()