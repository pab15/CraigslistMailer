# Test Email By Running this File!
# Import this File to Send Custom Emails

import sqlite3
import smtplib, ssl



def send_email(recipient_list, title, listing):
  for recipient in recipient_list:
    port = 465
    # Create 'Burner' Gmail Account
    # Enable 2FA
    # Add an App Password and Insert into the Password Field Below:
    smtp_server = "smtp.gmail.com"
    sender_email = 'declare@email.here'
    receiver_email = recipient
    password = "insert app password here"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.ehlo() 
        server.login(sender_email, password)
        subject = f'{title}'
        message = f'Subject: {subject}\n\n{listing}'
        server.sendmail(sender_email, receiver_email, message)

if __name__ == '__main__':
  # Send Email, Insert Target Email Below: 
  send_email(['add@testemail.here'], 'hello', 'message')
  # DO NOT USE ICLOUD, MESSAGES ARE FLAGGED IMMEDIATELY
  # Yahoo and Gmail recievers have been tested and used