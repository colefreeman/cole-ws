This block reads previously saved Magic card data from your SQLite database back into a Pandas DataFrame.
It includes automatic handling of binary data and encoding issues that might arise from stored card text.

The code defaults to reading from `mtg.db` and table `magic_cards`, but can be configured to read
from any SQLite database and table name.

Press "Play" to load your saved card data back into memory.