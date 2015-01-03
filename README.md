DJGE
====

### TODO
* Move encounter.funcs to encounter.models.Battle.methods
* Add world.models.Location.get_npcs('attitude') to return any NPCs that spawn at that location matching given attitude
* Make it possible to link multiple mobile.categories to a single world.location so we can spawn
 multiple types of combatants during random encounters.
* """Mobiles have a category, that category has a spawn point, if the current destination appears in the spawn points
  of ANY NPCs then spawn those NPCs.""" This is makes sense in the soft grey matter but is very convoluted in code.
* create /djge/dice.py roll(chance=100) where chance is 1-100 but use giant numbers in the actual function,
  and return bool
* Charecter/equip weapon, dropdown, queryset=Items.obj.filter(character).filter(offense)
* pacifist system, value in battle model, code in battlestack
* kill type count belongs to account, store it in player.models.Config, use throughs
* rename 'playing_toon' to 'playing_character'
* The (user|character)_is blocks are not DRY
