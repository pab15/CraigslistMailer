import sqlite3

# Run This File to Edit DB

def add_user():
  # Remember To add Path to db below:
  conn = sqlite3.connect(r'cars.db')

  username = input('Enter an username: ')
  email = input('Enter an email: ')
  min_price = input('Enter a min price: ')
  max_price = input('Enter a max price: ')
  postal_code = input('Enter a Postal Code: ')
  distance = input('Enter a distance from postal: ')
  postal_code = str(postal_code)
  distance = str(distance)
  min_price = str(min_price)
  max_price = str(max_price)
  c = conn.cursor()
  c.execute(f'''INSERT INTO users VALUES ('{username}', '{email}', '{min_price}', '{max_price}', '{postal_code}', '{distance}')''')
  conn.commit()
  conn.close()
  print(f'User <{username}> was Added Successfully!')

def delete_user(string_username):
  # Remember To add Path to db below:
  conn = sqlite3.connect(r'cars.db')
  c = conn.cursor()
  c.execute(f'''DELETE FROM users WHERE name=?''',(string_username,))
  conn.commit()
  conn.close()
  print(f'User <{string_username}> was Deleted Successfully!')

def delete_car(url):
  # Remember To add Path to db below:
  conn = sqlite3.connect(r'cars.db')
  c = conn.cursor()
  c.execute('''DELETE FROM car WHERE url=?''', (url,))
  conn.commit()
  conn.close()
  print(f'Car <{url}> was Deleted Successfully!')

def query():
  # Remember To add Path to db below:
  conn = sqlite3.connect(r'cars.db')
  c = conn.cursor()
  c.execute('''SELECT * FROM users''')
  data = c.fetchall()
  conn.close()
  return data

if __name__ == '__main__':
  # Easy to use, Just Run:
  remove_user = input('Remove a User? (y/N)')
  if remove_user == 'y' or remove_user == 'Y':
    user_to_delete = input('Enter the Username to remove: ')
    delete_user(user_to_delete)
  else:
    remove_car = input('Remove a Car? (y/N)')
    if remove_car == 'y' or remove_car == 'Y':
      remove_link = input('Enter a Link to Remove From DB: ')
      delete_car(remove_link)
    else:
      make_query_user = input('Query all Users? (y/N)')
      if make_query_user == 'y' or make_query_user == 'Y':
        print(query())
      else:
        add_a_user = input('Add a User? (y/N)')
        if add_a_user == 'y' or add_a_user == 'Y':
          add_user()
