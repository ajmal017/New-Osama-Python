# 7-1-2020
def start():
    name1 = str.capitalize(input("Please Enter Your Name:"))
    print("Hello", name1)
    print("~" * 10, "Now We Will Learn Some Times Table", "~" * 10)


def ope():
    num1 = int(input("Please Enter Number Less Than 13:"))
    if num1 < 13:
        time_tables(num1)
    else:
        print("Please Enter Number Lase Than 13")


def time_tables(num1):
    for x in range(1, 3):
        print(num1, "X", x, "=")
        num2 = int(input("Enter Answer:"))
        if num2 == num1 * x:
            print("Correct Answer")
        else:
            for y in range(1, 3):
                print("It's Wrong")
                print("Let Us Try Again")
                print(num1, "*", x, "=")
                num2 = int(input("Enter Answer:"))
                if num2 == num1 * x:
                    print("Correct Answer")
                    break
                else:
                    print("The Correct Answer Is =", num1 * x)
    choice = str(input(('are you went try anther table or Exit:Y\E')))
    if choice == 'y':
        print('Hello again')
        ope()
    else:
        print('Thank You for')


start()
ope()
