import re
import ssl
import urllib
import sqlite3
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
from urlmanager import *
from emailhandler import *

# This Function Finds All Links For Listings
# Given a Custom Url (I Build this With The Custom Search Functions)
# Returns Array of Links
def findCarLinks(craigslist_url):
    result = []
    response = urllib.request.urlopen(craigslist_url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.find_all('a', attrs={'class':'result-title hdrlnk'})

    result = [link.get('href') for link in links]
    return result

# Next Part Used in Previous Craigslist Project, Some Functionality 
# is Pointless, But Could be Used To Potentialy Improve Emails

# Function Takes a Listing Url, and Essentially Parses The Meta Data/
# Imformation for the Listing, Returning Everything as a Dictionary
def parsePages(page_url):
    result = {}

    response = urllib.request.urlopen(page_url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    result['url'] = page_url
    info = soup.find_all('b')
    pic_link = soup.find_all('img', attrs={'title':'1'})
    try:
        pic_link[0].get('src')
    except:
        result['pic'] = ""
    else:
        result['pic'] = pic_link[0].get('src')
    counter = 1
    for piece in info:
        new_piece = piece.parent.getText().encode('ascii', 'ignore').decode('utf-8')
        split_pieces = new_piece.split(':')
        if counter > 1:
            try:
                split_pieces[1] = split_pieces[1].replace(" ", "", 1)
                result[split_pieces[0]] = split_pieces[1]
            except:
                print('badcarvalue')
            else:
                split_pieces[1] = split_pieces[1].replace(" ", "", 1)
                result[split_pieces[0]] = split_pieces[1]
        else:
            result['car'] = split_pieces[0]
            try:
                int(split_pieces[0][0:4]) 
            except:
                result['model year'] = ""
            else:
                result['model year'] = split_pieces[0][0:4]
            price = soup.find_all('span', attrs={'class':'price'})
            try:
                price[0].string.strip('$')
            except:
                result['price'] = '0'
                result['model year'] = ""
            else:
                result['price'] = price[0].string.strip('$')

        counter += 1
    return result

if __name__ == '__main__':
    # Make sure path to db is specified on Linux:
    # Create DB Connection and Cursor:
    conn = sqlite3.connect('cars.db')
    c = conn.cursor()

    # Create Tables for DB, Used for Tossing Out
    # Previously Mailed Urls
    # Also Allows Storage of User Emails and Requested Criteria
    c.execute('''CREATE TABLE IF NOT EXISTS car
                (url STRING)''')
    c.execute('''CREATE TABLE IF NOT EXISTS goodlinks
                (url STRING)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (name STRING, email STRING, minprice STRING, maxprice STRING)''')
    
    # Query all the names of Users
    c.execute("SELECT name FROM users")

    # Store as array:
    allusers = c.fetchall()

    # Loop through every user
    for u in allusers:
        # Query their data (email and search criteria)
        # and store values as variables
        name = u[0]
        c.execute("SELECT * FROM users WHERE name = ?", (name,))
        userinfo = c.fetchone()
        user_name = userinfo[0]
        user_email = userinfo[1]
        user_min_price = str(userinfo[2])
        user_max_price = str(userinfo[3])
        user_postal = str(userinfo[4])
        user_distance = str(userinfo[5])

        # Prints for Debugging:
        print(user_name)
        print(user_email)
        print(user_min_price)
        print(user_max_price)

        # Build our custom Url:
        url = urlManager('sfbay', 'owner') + postedToday() + addMinPrice(user_min_price) + addMaxPrice(user_max_price) + addPostal('94804') + addDistance('20')

        # Find all listings with given criteria and print for debugging:
        array = findCarLinks(url)
        print(array)

        # Loop through individual listings:
        for link in array:
            #Print to make sure we entered the loop:
            print(link)

            # Try to find the Url in DB:
            c.execute("SELECT rowid FROM car WHERE url = ?", (link,))
            data=c.fetchone()

            # If URL does not Exist:
            if data is None:
                # Insert value into DB
                ## ERROR HERE: if two users have overlapping price ranges, 
                ###            then another user should not get the email,
                ##             as it should be added to DB and committed and checked 
                ##             when that users criteria is being looped through
                ## HOWEVER: Although this error should occur, it does not.
                ##          I get the same emails my friend does.
                ##          I also get listings from his range that are not in mine
                ##          This should not happen
                c.execute(f"INSERT INTO car VALUES ('{link}')")
                conn.commit()

                # Parse the current link and get the dictionary of meta data
                info = parsePages(link)

                # Check for title status
                if 'title status' in info.keys():
                    # Make sure we entered the conditional, print to verify:
                    print(info)

                    # We only are interested in clean titles, salvaged cars are a 
                    # bitch and a half to insure
                    if info['title status'] == 'clean':
                        # If its clean and matches our criteria, grab that email again:
                        # Shouldn't need to do this, but I need a list to pass to my send 
                        # mail function
                        c.execute("SELECT email FROM users WHERE name = ?", (user_name,))
                        user = c.fetchall()

                        # Print to make sure we got an array
                        print(user_email)

                        # Send that email!
                        send_email(str(user_email), info['car'], link)

                        # Add to good links, IDK why I did this, future reference I guess
                        c.execute(f"INSERT INTO goodlinks VALUES ('{link}')")
                        print(info)
                    else:
                        # Car is salvaged so we print to debug
                        # and pass it up
                        print('salvaged')
                        
                # Make sure we're committing our db changes
                conn.commit()
            else:
                # We Found The Listing So just print to debug:
                print('found in db')

    # Commit once more and close connection:
    conn.commit()
    conn.close()