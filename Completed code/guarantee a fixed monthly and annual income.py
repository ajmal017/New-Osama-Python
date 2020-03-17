"""A program for calculating the value of what you need to deposit with the bank now
 in order to guarantee a fixed monthly and annual income throughout a certain number of years"""
me = monthly_expense = int(input('Please Enter Monthly expense '))
ae = annual_expense = int(input('Please Enter The annual expense '))
annual_increase_rate = int(input('Please Enter Annual increase rate'))
annual_bank_interest_rate = int(input('Please Enter Annual bank interest rate '))
monthly_interest_rate = annual_bank_interest_rate / 1200
number_of_years = int(input('Please Enter Number of years '))
# print('No. of\nYears\t', ' Start\t\t', '1\t\t', '  2\t', '  3\t', '   4\t', '    5\t\t', '6\t\t', '  7\t', '   8\t', '   9\t', '     10\t', '  11\t', '    12\t', 'A. Expense', 'M.Expense')
for start in range(2000000, 3000000):
    monthly_expense = me
    annual_expense = ae
    fff = start
    for x in range(0, number_of_years):
        monthly = [start]
        for y in range(0, 12):
            c = (start * (1 + annual_bank_interest_rate / 1200)) - monthly_expense
            start = c
            monthly.append(int(c))
        start = int(monthly[12] - annual_expense)
        monthly_expense = monthly_expense * (1 + annual_increase_rate / 100)
        annual_expense = annual_expense * (1 + annual_increase_rate / 100)
        if x == (number_of_years - 1) and (200 > monthly[0] > -200):
            # print(x + 1, "\t\t", monthly, "\t", int(monthly_expense), "\t", int(annual_expense))
            print("The value of what you need to deposit with the bank now for", x, "Years", fff)
