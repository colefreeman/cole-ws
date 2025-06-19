from typing import Dict, List

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer


@transformer
def transform(messages: List[Dict], *args, **kwargs):
   """
   Calculate directional trade values to track buying vs selling pressure
   
   Args:
       messages: List of messages in the stream.
   Returns:
       Transformed messages with buy/sell pressure calculations and price totals
   """
   
   # Sort messages by timestamp and symbol to maintain order
   messages_sorted = sorted(messages, key=lambda x: (x['symbol'], x['timestamp']))
   
   # Track running totals per symbol
   symbol_totals = {}
   
   for message in messages_sorted:
       symbol = message['symbol']
       price = message['price']
       quantity = message['quantity']
       
       # Initialize symbol tracking if not exists
       if symbol not in symbol_totals:
           symbol_totals[symbol] = {'cumulative_price': 0, 'trade_count': 0}
       
       # Basic trade value (price × quantity)
       trade_value_usd = price * quantity
       message['trade_value_usd'] = trade_value_usd
       
       # Directional values based on trade side
       # buyer_maker = True means market sell order (bearish)
       # buyer_maker = False means market buy order (bullish)
       
       if message['buyer_maker']:
           # This is a sell order
           message['buy_value'] = 0
           message['sell_value'] = trade_value_usd
           message['trade_side'] = 'SELL'
       else:
           # This is a buy order
           message['buy_value'] = trade_value_usd
           message['sell_value'] = 0
           message['trade_side'] = 'BUY'
       
       # Net buying pressure (positive = more buying, negative = more selling)
       message['net_buy_pressure'] = message['buy_value'] - message['sell_value']
       
       # Cumulative price totals
       symbol_totals[symbol]['cumulative_price'] += price
       symbol_totals[symbol]['trade_count'] += 1
       
       message['cumulative_price_total'] = symbol_totals[symbol]['cumulative_price']
       message['average_price'] = symbol_totals[symbol]['cumulative_price'] / symbol_totals[symbol]['trade_count']
   
   print(f"Processed {len(messages)} trades with directional values and price totals")
   
   return messages
