import random

# Enable emailing
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Read mailing list
def read_mailing_list():
    searching = True
    numUsers = 0
    EMAIL_MAILING_LIST = []

    f = open("mailing-list.txt", 'r')
    lines = f.read().splitlines()

    # Add users to mailing list
    while searching:
        try:
            if lines[0 + numUsers] == "":
                searching = False
            else:
                EMAIL_MAILING_LIST.append(lines[0 + numUsers])
                numUsers += 1
        # If there are no more lines in the mailing list file
        # Then there are no more user to mail to
        except IndexError:
            searching = False

    f.close()

    return EMAIL_MAILING_LIST

# Pick random update to email
def get_random_update(updates):
    rand_index = random.randint(0, len(updates) - 1)
    update = updates[rand_index]

    return update

# Format text for email
def format_update(update):
    formatted_update = update

    return formatted_update

# Send update as email
def email_update(formatted_update, mailing_list):
    name = formatted_update[0]
    update = formatted_update[1]

    # Read email credentials from external file
    f = open("AuthenticationCredentials.txt","r")
    lines = f.read().splitlines()
    EMAIL_USERNAME = lines[1]
    EMAIL_PASSWORD = lines[2]
    f.close()

    userIndex = 0

    while userIndex < len(mailing_list):

        # Email results to self
        fromaddr = EMAIL_USERNAME
        toaddr = mailing_list[userIndex]

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
        userIndex += 1

# Main
def send_update(updates):
    mailing_list = read_mailing_list()
    update = get_random_update(updates)
    formatted_update = format_update(update)
    email_update(formatted_update, mailing_list)
