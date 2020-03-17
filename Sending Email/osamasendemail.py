"""
import csv
import yagmail

emails = []
names = []
with open("contacts_file.csv") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for name, email, grade in reader:
        emails.append(email)
        names.append(name)
yag_smtp_connection = yagmail.SMTP(user="osamapython@gmail.com", password="Os01265065()", host='smtp.gmail.com')
subject = 'Hello from Osama'
for x in range(len(names)):
    message = f"Hi Mr. {names[x].capitalize()}, it's just a test Message."
    contents = [message, 'D:\Python\Project\OsamaPython\image.jpg', 'D:\Python\Project\OsamaPython\message.txt']
    yag_smtp_connection.send(emails[x], subject, contents)
print('Sent ........')
"""
import csv
import yagmail

attachments = []
emails = []
names = []
receiver_file = input("Please enter a Path of  file containing the e-mails to be sent like this 'D:\Docu\mycontact.cvs ' :")
with open(receiver_file) as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    for name, email, grade in reader:
        emails.append(email)
        names.append(name)
print(names)
your_email = input('Please Enter Your Email')
your_password = input('Please Enter Your Password')
yag_smtp_connection = yagmail.SMTP(user=your_email, password=your_password, host='smtp.gmail.com')
subject = input("Please Enter Subject Here")
number_of_attachments = int(input("Please Enter Number of files attached:"))
for x in range(number_of_attachments):
    attached = input("Please enter a Path of  file you want a attached like this 'D:\Docu\myattached' :")
    attachments.append(attached)
print(attachments)
for x in range(len(names)):
    message = f"Hi Mr. {names[x].capitalize()}, it's just a test Message."
    contents = [message, 'D:\Python\Project\OsamaPython\image.jpg', 'D:\Python\Project\OsamaPython\message.txt']
    yag_smtp_connection.send(emails[x], subject, contents)
print('Sent ........')
