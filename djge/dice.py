"""
djge/dice.py
"""
import random


def roll(chance, debug=False):
    """
    chance = a float, (1.000000 to 100.000000), represents the percent of success.
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
            print('{0} is less than {1} of max {2}'.format(rolled, chance, ceiling))
        return True
    if debug is True:
        print('{0} not less than {1}, max {2}'.format(rolled, chance, ceiling))
    return False


def examples():
    """
    Roll a few times to show how it works.
    """
    print('99.999998% chance roll, debug is True')
    print(roll(chance=99.999998, debug=True))

    print('50.000001% chance roll, debug is True')
    print(roll(50.000001, debug=True))

    print('50% chance roll, debug is False')
    print(roll(50))

    print('Roll 900900 times, with 0.123% chance for success, show successful rolls.')
    for i in range(900900):
        if roll(0.0123):
            print(i)


if __name__ == '__main__':
    examples()
