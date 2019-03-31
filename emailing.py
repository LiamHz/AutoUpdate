import random

# Enable emailing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Pick random update to email
def get_random_update(updates):
    rand_index = random.randint(0, len(updates))
    update = updates[rand_index]

    return update

# Format text for email
def format_update(update):
    formatted_update = update

    return formatted_update

# Send update as email
def email_update(formatted_update):
    name = formatted_update[0]
    update = formatted_update[1]

    # Read email credentials from external file
    f = open("AuthenticationCredentials.txt","r")
    lines = f.read().splitlines()
    EMAIL_USERNAME = lines[1]
    EMAIL_PASSWORD = lines[2]
    f.close()

    # Email results to self
    fromaddr = EMAIL_USERNAME
    toaddr = EMAIL_USERNAME

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = f"{name}'s Weekly Update'"

    # Allow Unicode characters to be emailed
    plainText = MIMEText(update.encode('utf-8'), 'plain', 'UTF-8')
    # html = MIMEText(html, 'html')

    msg.attach(plainText)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, EMAIL_PASSWORD)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

    print("Sent email to", toaddr)

# Main
def send_update(updates):
    update = get_random_update(updates)
    formatted_update = format_update(update)
    email_update(formatted_update)
