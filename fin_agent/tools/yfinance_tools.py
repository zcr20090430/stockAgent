import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_daily_price_yf(symbol, start_date=None, end_date=None, market='CN'):
    """
    Get daily stock price using yfinance.
    :param symbol: Stock code (e.g., '000001' for A股, 'AAPL' for US stock)
    :param start_date: Start date (YYYY-MM-DD or YYYYMMDD)
    :param end_date: End date (YYYY-MM-DD or YYYYMMDD)
    :param market: Market identifier ('CN' for China A股, 'US' for US stocks, 'HK' for Hong Kong)
    :return: JSON string
    """
    try:
        ticker_symbol = _format_symbol(symbol, market)
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        else:
            start_date = _format_date(start_date)
        
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            end_date = _format_date(end_date)
        
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start=start_date, end=end_date)

        
        if df.empty:
            return f"No data found for {ticker_symbol} between {start_date} and {end_date}."
        
        df = df.reset_index()
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        df = df.rename(columns={
            'Date': 'trade_date',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'vol'
        })
        
        df = df[['trade_date', 'open', 'high', 'low', 'close', 'vol']]
        df = df.sort_values('trade_date', ascending=False)
        
        return df.to_json(orient='records', force_ascii=False)
    except Exception as e:
        return f"Error fetching daily price from yfinance: {str(e)}"

def _format_symbol(symbol, market='CN'):
    """
    Format symbol for yfinance based on market.
    :param symbol: Original stock code
    :param market: Market identifier
    :return: Formatted symbol for yfinance
    """
    symbol = symbol.strip().upper()
    
    if market == 'CN':
        if '.' in symbol:
            code, exchange = symbol.split('.')
            if exchange == 'SH':
                return f"{code}.SS"
            elif exchange == 'SZ':
                return f"{code}.SZ"
        else:
            if symbol.startswith('6'):
                return f"{symbol}.SS"
            else:
                return f"{symbol}.SZ"
    elif market == 'HK':
        if not symbol.endswith('.HK'):
            return f"{symbol}.HK"
    elif market == 'US':
        return symbol
    
    return symbol

def _format_date(date_str):
    """
    Format date string to YYYY-MM-DD.
    :param date_str: Date string (YYYYMMDD or YYYY-MM-DD)
    :return: Formatted date string (YYYY-MM-DD)
    """
    date_str = str(date_str).strip()
    
    if '-' in date_str:
        return date_str
    elif len(date_str) == 8:
        return f"{date_str[0:4]}-{date_str[4:6]}-{date_str[6:8]}"
    else:
        return date_str

def get_stock_info_yf(symbol, market='CN'):
    """
    Get stock basic information using yfinance.
    :param symbol: Stock code
    :param market: Market identifier
    :return: JSON string
    """
    try:
        ticker_symbol = _format_symbol(symbol, market)
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        
        if not info:
            return f"No information found for {ticker_symbol}."
        
        result = {
            'symbol': ticker_symbol,
            'name': info.get('longName', info.get('shortName', 'N/A')),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'currency': info.get('currency', 'N/A')
        }
        
        return pd.DataFrame([result]).to_json(orient='records', force_ascii=False)
    except Exception as e:
        return f"Error fetching stock info from yfinance: {str(e)}"

YFINANCE_TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_daily_price_yf",
            "description": "Get historical daily price data using yfinance (supports A-shares, US stocks, HK stocks). This is an alternative to tushare's get_daily_price and does not require tushare token.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock code (e.g., '000001' for A股, 'AAPL' for US stock, '00700' for HK stock)"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD or YYYYMMDD format. Defaults to 30 days ago."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date in YYYY-MM-DD or YYYYMMDD format. Defaults to today."
                    },
                    "market": {
                        "type": "string",
                        "description": "Market identifier: 'CN' for China A股, 'US' for US stocks, 'HK' for Hong Kong. Defaults to 'CN'.",
                        "enum": ["CN", "US", "HK"]
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_info_yf",
            "description": "Get basic stock information using yfinance (name, sector, industry, market cap). Alternative to tushare's get_stock_basic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock code (e.g., '000001' for A股, 'AAPL' for US stock)"
                    },
                    "market": {
                        "type": "string",
                        "description": "Market identifier: 'CN' for China A股, 'US' for US stocks, 'HK' for Hong Kong. Defaults to 'CN'.",
                        "enum": ["CN", "US", "HK"]
                    }
                },
                "required": ["symbol"]
            }
        }
    }
]

if __name__ == "__main__":
    print(get_daily_price_yf('000001', '2023-01-01', '2023-01-31'))
    print(get_stock_info_yf('000001'))
