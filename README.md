# CraigslistMailer

I wrote this script to grab new car listings and notify me by email whenever I there is a new car listed that matches my criteria. This saves me time because I get a notification for new cars, and don't have to constantly refresh craigslist and search through it manually. It also slightly cuts out results that are a waste of my time.
I run this on a Raspberry Pi and I use a cron job to keep it going every 10 minutes. 
I am posting this because I want other people to try it and improve it.

Requirements:
- Python 3.5+
- Beautiful Soup 
- Gmail Account with 2FA and an app password configured

Pip:
- pip install beautifulsoup4

Make sure you add yourself as a user! You can use something like SQLite Studio, or you can use the adduser.py script:
- `python3 adduser.py # This should hopefully be pretty straight forward`

Setup Cron:
- Make the craigslistparser file executable:
- `sudo chmod +X craigslistparser.py`

- Open chrontab to add chron job and set time:
- `sudo crontab -e`

- Add Line:
- `*/10 * * * * /path/to/file/craigslistparser.py`

- Done! Script will be executed every 10 minutes, assuming no errors