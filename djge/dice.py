"""
djge/dice.py
"""
import random


def roll(chance, debug=False):
    """
    """
    chance = float(chance)
    if chance >= 100:
        return True
    if chance <= 0:
        return False
    ceiling = 100000000
    chance *= 1000000
    chance = int(chance)
    rolled = random.randint(1, ceiling)
    if rolled < chance:
        if debug is True:
            print('{0}<{1}/{2}'.format(rolled, chance, ceiling))
        return True
    if debug is True:
        print('{0}>{1}/{2}'.format(rolled, chance, ceiling))
    return False


# print(roll(chance=99.999998, debug=True))
# print(roll(50.000001, debug=True))
# print(roll(50))

"""
for i in range(900900):
    if roll(0.0123):
        print(i)
"""
