""""
# Mutations
def mutate_string(string, position, character):
    k = list(string)
    k[position] = character
    string = ''.join(k)
    return print(string)


mutate_string('abracadabra', 5, 'k')


# String Validators
s = 'qA2'
s = list(s)
for x in s:
    if x.isalnum():
        print(x.isalnum())
        break
    else:
        print(False)
for x in s:
    if x.isalpha():
        print(x.isalpha())
        break
for x in s:
    if x.isdigit():
        print(x.isdigit())
        break
for x in s:
    if x.islower():
        print(x.islower())
        break
for x in s:
    if x.isupper():
        print(x.isupper())
        break

"""

s = '999'

print(any(c.isalnum() for c in s))
print(any(c.isalpha() for c in s))
print(any(c.isdigit() for c in s))
print(any(c.islower() for c in s))
print(any(c.isupper() for c in s))
