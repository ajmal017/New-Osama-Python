"""
Variables and Strings:Variables are used to store values. A string is a series of characters, surrounded by single or double quotes """
# Hello world
print("Hello world!")
#Hello world with a variable
msg = "Hello world!"
print(msg)
#f strings (using variables in strings)
first_name = 'albert'
last_name = 'einstein'
full_name = f"{first_name} {last_name}"
print(full_name)
###########################################################################################
"""  Lists: A list stores a series of items in a particular order. You access items using an index, or within a loop.
What are lists?
A list stores a series of items in a particular order.Lists allow you to store sets of information in one 
place, whether you have just a few items or millions of items. Lists are one of Python's most powerful
features readily accessible to new programmers, and they tie together many important concepts in programming """
# Make a list
bikes = ['trek', 'redline', 'giant']
# Get the first item in a list
first_bike = bikes[0]
# Get the last item in a list
last_bike = bikes[-1]
# Looping through a list
for bike in bikes:
print(bike)
#Adding items to a list
bikes = []
bikes.append('trek')
bikes.append('redline')
bikes.append('giant')
#Making numerical lists
squares = []
for x in range(1, 11):
squares.append(x**2)
# List comprehensions
squares = [x**2 for x in range(1, 11)]
#Slicing a list
finishers = ['sam', 'bob', 'ada', 'bea']
first_two = finishers[:2]
#Copying a list
copy_of_bikes = bikes[:]
###############################################################################################
# Tuples : Tuples are similar to lists, but the items in a tuple can't be modified.
#Making a tuple
dimensions = (1920, 1080)
If statements
If statements are used to test for particular conditions and
respond appropriately.
Conditional tests
equals x == 42
not equal x != 42
greater than x > 42
or equal to x >= 42
less than x < 42
or equal to x <= 42
Conditional test with lists
'trek' in bikes
'surly' not in bikes
Assigning boolean values
game_active = True
can_edit = False
A simple if test
if age >= 18:
print("You can vote!")
If-elif-else statements
if age < 4:
ticket_price = 0
elif age < 18:
ticket_price = 10
else:
ticket_price = 15
Python Crash Course
A Hands-On, Project-Based
Introduction to Programming
nostarch.com/pythoncrashcourse2e
Dictionaries
Dictionaries store connections between pieces of
information. Each item in a dictionary is a key-value pair.
A simple dictionary
alien = {'color': 'green', 'points': 5}
Accessing a value
print(f"The alien's color is {alien['color']}")
Adding a new key-value pair
alien['x_position'] = 0
Looping through all key-value pairs
fav_numbers = {'eric': 17, 'ever': 4}
for name, number in fav_numbers.items():
print(f"{name} loves {number}")
Looping through all keys
fav_numbers = {'eric': 17, 'ever': 4}
for name in fav_numbers.keys():
print(f"{name} loves a number")
Looping through all the value