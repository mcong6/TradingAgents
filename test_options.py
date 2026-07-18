import sys
import os

sys.path.append(os.path.abspath('.'))

from tradingagents.dataflows.y_finance import get_options_data
try:
    print("Testing Options Data for AAPL...")
    result = get_options_data("AAPL")
    print(result)
except Exception as e:
    print("Error:", e)
