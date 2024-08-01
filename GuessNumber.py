import random

guessNumber = random.randint(1,100)
#print(guessNumber)



while(True) :
    try :
        print("please input a number:")
        number = int(input())
    except Exception as e:
        print("input is not a number, please input again")
        continue

    if (guessNumber == number):
        print("correct")
        break
    elif (guessNumber > number):
        print("big")
    elif (guessNumber < number):
        print("small")

