"""

        self.Fnks = []
        self.Fnks.append([int(100), 'Total',             'Funks Total %'])
        self.Fnks.append([int(34),  'Extra Dodge',       'Dodge if monster would hit. (class=Any,level=1)'])
        self.Fnks.append([int(33),  'Double Damage',     'Double damage if you hit. (class=Any,level=1)'])
        self.Fnks.append([int(0),   'Double Funk Regen', 'checked during funk regen after you finish an attack
        self.Fnks.append([int(33),  'Auto-Heal (magic)', 'heal self after monster attack, before your attack.
        self.Fnks.append([int(0),   'Auto-Steal',        'steal money/items from monster after successful attack
        self.Fnks.append([int(0),   'Extra Attack',      'add another swing during attack, damage cannot be doubled
        self.Fnks.append([int(0),   'Extra Heal',        'Chance to boost healing. Works during Auto-Heal, too.'])


"""
import random


def attack(self, attacker, target):
    if random.randint(0, 1024) <= 256:
        return False
    base_damage = attacker.base_offense
    try:
        equipped_damage = attacker.equip_offense.base.power
    except:
        equipped_damage = 0
    total_damage = base_damage + equipped_damage
    # if autoact.doubledamage(attacker):
    #     total_damage *= 2
    target.life -= total_damage
    target.save()
    return total_damage


def heal_self(character_is):
    diff = character_is.life_max - character_is.life
    character_is.life = character_is.life_max
    character_is.save()
    return diff
