import string
import random  # define the random module

def get_keys(num: int):
    """ num is an int value. that decides how many caracters would be generated"""
    # call random.choices() string module to find the string in Uppercase + numeric data.
    _ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=num))
    return str(_ran)