import yagmail
import csv

attachments = []
emails = []
names = []
# receiver_file = input("Please enter a Path of  file containing the e-mails to be sent like this 'D:\document\mycontact.cvs ' :")
receiver_file = input("Please enter a Path of  file containing the e-mails to be sent like this 'D:\document\mycontact.cvs ' :")
with open(receiver_file) as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for name, email, grade in reader:
        emails.append(email)
        names.append(name)
your_email = input('Please Enter Your Email:')
your_password = input('Please Enter Your Password:')
yag_smtp_connection = yagmail.SMTP(user=your_email, password=your_password, host='smtp.gmail.com')
subject = input("Please Enter Subject Here:")
no_of_attachments = int(input("Please Enter No.of Attachments"))
for x in range(no_of_attachments):
    attached = input(f'Please Enter path for  attached No.{x + 1}:')
    attachments.append(attached)
message = input("Enter Your message Here:")
for x in range(0, len(names)):  # Loop to change the name to match the owner of the email
    attachments.insert(0, f'Hi {names[x].capitalize()} {message.capitalize()}')
    contents = attachments.copy()
    attachments.pop(0)
    yag_smtp_connection.send(emails[x], subject, contents)
print('Sent ........')
