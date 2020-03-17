# 1-Sending emails to a list of people  HTML
"""
import smtplib
import ssl
from email.mime.text import MIMEText  # New line
from email.utils import formataddr  # New line

# User configuration
sender_email = 'osamapython@gmail.com'
sender_name = 'osama'
password = 'Os01265065()'

receiver_emails = ['sgrcairo@gmail.com', 'groupohn@gmail.com']
receiver_names = ['RECEIVER_NAME_1', 'RECEIVER_NAME_2']

# Email text
email_body = '''
    This is a test email sent by Python. Isn't that cool?
'''

for receiver_email, receiver_name in zip(receiver_emails, receiver_names):
    print("Sending the email...")
    # Configurating user's info
    msg = MIMEText(email_body, 'plain')
    msg['To'] = formataddr((receiver_name, receiver_email))
    msg['From'] = formataddr((sender_name, sender_email))
    msg['Subject'] = 'Hello, my friend ' + receiver_name
    try:
        # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # Encrypts the email
        context = ssl.create_default_context()
        server.starttls(context=context)
        # We log in into our Google account
        server.login(sender_email, password)
        # Sending email from sender, to receiver with the email body
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent!')
    except Exception as e:
        print(f'Oh no! Something bad happened!n {e}')
    finally:
        print('Closing the server...')
        server.quit()


##################################################################################################################
# 2-Sending to Multiple Emails with attached file
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

email = 'osamapython@gmail.com'
password = 'Os01265065()'
send_to_emails = ['sgrcairo@gmail.com', 'groupohn@gmail.com']  # List of email addresses
subject = 'This is the subject'
message = 'This is my message'
file_location = 'C:\\Users\\osama\\Desktop\\mycontacts.txt'

# Create the attachment file (only do it once)
filename = os.path.basename(file_location)
attachment = open(file_location, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# Connect and login to the email server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)

# Loop over each email to send to
for send_to_email in send_to_emails:
    # Setup MIMEMultipart for each email address (if we don't do this, the emails will concat on each email sent)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))
    # Attach the attachment file
    msg.attach(part)

    # Send the email to this specific email address
    server.sendmail(email, send_to_email, msg.as_string())

# Quit the email server when everything is done
server.quit()
##################################################################################################################


# 3-A function to split the email into the name and email form .txt file
def get_contacts(filename):
    emails = []
    names = []

    with open(filename) as contacts_file:
        for a_contact in contacts_file.readlines():
            txt = a_contact.strip().split(',')
            print(txt)
            name = txt[0].split('@')[0]
            email = txt[0].split(',')
            names.append(name)
            emails.append(email)
        emails.pop()



    return emails,names


# When you call the function, pass the file path as an argument
print(get_contacts('Test for email16.txt'))  # must test.txt file in the same folder with python file (New Send Email) and do not forget quota(')
# print(get_contacts('C:\\Users\\osama\Desktop\\Test for email13.txt'))  # او ضع مسار الملف لو مش فى نفس الفولدر مع ملف البايثون


##################################################################################################################
# Function to read the contacts from a given contact file and return a
# list of names and email addresses
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split('@')[0])
            emails.append(a_contact.split())
    return emails, names


print(get_contacts('Test for email14.txt'))
"""
##################################################################################################################
# Sending to Multiple Emails with attached file  وبياخد الايميلات من دالة بتاخدهم من ملف txt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path


def get_contacts(filename):
    emails = []
    names = []

    with open(filename) as contacts_file:
        for a_contact in contacts_file.readlines():
            txt = a_contact.strip().split(',')
            emails.append(txt[0])
            name = txt[0].split('@')[0]
            names.append(name)

    return names,emails

names, emails = get_contacts('mycontacts.txt')
print("you will sent Email To :",emails)
email = 'osamapython@gmail.com'
password = 'Os01265065()'
send_to_emails = emails  # List of email addresses take it from get_contacts
subject = 'This is the subject'
message = 'This is my message'
file_location = 'C:\\Users\\osama\\Desktop\\mycontacts.txt'

# Create the attachment file (only do it once)
filename = os.path.basename(file_location)
attachment = open(file_location, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

# Connect and login to the email server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)

# Loop over each email to send to
for send_to_email in send_to_emails:
    # Setup MIMEMultipart for each email address (if we don't do this, the emails will concat on each email sent)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))
    # Attach the attachment file
    msg.attach(part)

    # Send the email to this specific email address
    server.sendmail(email, send_to_email, msg.as_string())

# Quit the email server when everything is done
server.quit()
