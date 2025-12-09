
This block handles saving your Magic card data into a SQLite database for persistent storage.
It includes automatic encoding cleanup to handle special characters and symbols commonly found in card text.


The code will create a new SQLite database if it doesn’t exist, or update an existing one.
By default, it saves to `mtg.db` with table name 'magic_cards'.


Press "Play" to execute this block after running the card loader to save your data.