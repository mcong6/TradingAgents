import logging
from typing import Annotated

from langchain_core.tools import tool

from tradingagents.dataflows.interface import route_to_vendor

logger = logging.getLogger(__name__)


@tool
def get_stock_data(
    symbol: Annotated[str, "ticker symbol of the company"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    Retrieve stock price data (OHLCV) for a given ticker symbol.
    Uses the configured core_stock_apis vendor.
    Args:
        symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
        start_date (str): Start date in yyyy-mm-dd format
        end_date (str): End date in yyyy-mm-dd format
    Returns:
        str: A formatted dataframe containing the stock price data for the specified ticker symbol in the specified date range.
    """
    logger.info(f"Executing tool get_stock_data for {symbol}")
    return route_to_vendor("get_stock_data", symbol, start_date, end_date)

@tool
def get_options_data(
    symbol: Annotated[str, "ticker symbol of the company"],
) -> str:
    """
    Retrieve options flow data (Put/Call ratio and highest Open Interest strikes) for a given ticker symbol.
    Uses the configured core_stock_apis vendor (e.g. yfinance).
    Args:
        symbol (str): Ticker symbol of the company, e.g. AAPL, TSM
    Returns:
        str: A formatted markdown string containing the nearest expiration options data, Put/Call Ratios, and Strike Walls.
    """
    logger.info(f"Executing tool get_options_data for {symbol}")
    return route_to_vendor("get_options_data", symbol)
