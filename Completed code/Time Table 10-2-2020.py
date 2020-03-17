# 3-2-2020
def start():  # function for start
    name1 = str.capitalize(input("Please Enter Your Name:"))
    print("Hello", name1)
    print("~" * 10, "Now We Will Learn Some Multiplication", "~" * 10)


def processing():  # function for operation
    num1 = int(input('Please Enter a Number Less Than 13:'))
    if num1 < 13:
        time_tables(num1)
        print('This Number Grate Than 13')
        processing()


def time_tables(num1):  # داله لحساب عملية الضرب
    for x in range(1, 13):
        print(num1, "X", x, "=")
        num2 = int(input("Enter Answer:"))
        if num2 == num1 * x:
            print("Good job!")

        else:
            for _ in range(1, 3):
                print(" It's Wrong Let's Try Again\n", num1, "*", x, "=")
                num2 = int(input("Enter Answer:"))
                if num2 == num1 * x:
                    print("Fantastic!")
                    break
            else:
                print("The Correct Answer Is =", num1 * x)
    choice = str(input('Do you Want to Try Another Time Table or Not?:Y Or N?'))
    if choice == 'y':
        print('Hello again')
        processing()
    else:
        print('Thank You for Coming')
        quit()


start()  # Start from here
processing()  # after start
