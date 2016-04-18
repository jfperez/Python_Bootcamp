#!/usr/bin/env python3
# Calculate the checksum of a credit card number
# and let the user know if the cc# entered is valid


def check_sum(num):
    # Checksum checker function
    chk_num = list(str(num))[::-1]
    count = 1
    # Double all the even elements of the list
    while count < len(chk_num):
        chk_num[count] = int(chk_num[count]) * 2
        count += 2
    num = ''.join(map(str, chk_num))
    count, total = 0, 0
    # Add each digit together
    while count < len(num):
        total += int(num[count])
        count += 1
    return total % 10 == 0

while True:
    try:
        num = input('Enter a 13-16 digit card # :')
        if len(num) == 0:
            exit()
        chk = check_sum(num)
        if chk:
            print("You entered a valid credit card #:")
        else:
            print("That was an invalid credit card #:")
        go = input("Enter another? (Y/N? ")
        if not len(go) or go.upper() not in 'Y':
            break
    except ValueError:
        print("That's not a # !!!")


