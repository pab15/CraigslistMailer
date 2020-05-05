import sqlite3

# Uneccessary Main Here for the Flex I Guess:
if __name__ == '__main__':
  # Allows you to add more columns, just change the column names:
  conn = sqlite3.connect("cars.db")
  c = conn.cursor()
  addColumn = "ALTER TABLE users ADD COLUMN minprice STRING"
  c.execute(addColumn)
  addColumn = "ALTER TABLE users ADD COLUMN maxprice STRING"
  c.execute(addColumn)
  conn.commit()
  conn.close()
  print('Done')