"""
A program for calculating the total amount deposited in the bank to cover the school
expenses completely throughout the school years, and the remainder is zero after the end of the
school years
"""

# (ver 1) account money and check it (12-2-2020 by Osama)
n1 = int(input('What is the value of the annual school expenses:'))
n2 = int(input('How many years will you spend in school:'))
n3 = float(input('What is the value of the annual bank interest:'))


def check(test):
    for _ in range(0, n2):
        test = test - n1
        for _ in range(0, 12):
            test += (test * (n3 / 1200))
    print('Pound differences:', int(test))


total_amount = []
for start in range(1, 1000000):  # It tests numbers until it reaches the required verification value
    remaining_amount = int(start)
    for a in range(0, n2):
        remaining_amount = remaining_amount - n1  # Deduction of the value of the first annual premium
        for _ in range(0, 12):
            remaining_amount += (remaining_amount * (n3 / (12 * 100)))
            # Calculating the monthly interest value on the deposited amount, noting that the annual interest has
            # been divided by the number of months of the year (12)
    if -20 < int(remaining_amount) < 20:
        # The remainder in the bank allowed after the end of the school years is from -20 to 20 Egyptian Pound (if
        # the value is negative, this value will be yours, even if it is positive, it will be for the school)
        total_amount.append(start)  # Group values that meet this condition in a list
sss = int(sum(total_amount) / len(total_amount))  # Average values
print('The total amount required to be deposited in the bank:', sss)
check(sss)
print('The total amount paid in the case of paying school fees annually:', n1 * n2)
print('The amount saved:', n1 * n2 - sss)
