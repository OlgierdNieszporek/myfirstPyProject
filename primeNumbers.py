from math import sqrt


def check_if_prime(number):
    isPrime = 0

    if (number > 1):
        for i in range(2, int(sqrt(number)) + 1):
            if (number % i == 0):
                isPrime = 1
                break
        if (isPrime == 0):
            return "Number is prime"
        else:
            return "Number is not prime"
    else:
        return "Number is not prime"
