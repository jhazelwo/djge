DJGE
====

### TODO
* """Mobiles have a category, that category has a spawn point, if the current destination appears in the spawn points
  of ANY NPCs then spawn those NPCs.""" This is makes sense in the soft grey matter but is very convoluted in code.
* Currently the idea of "\player\" includes ones account and characters but break them out in the interface:
* /my/account/
* /my/characters/
* Charecter/equip weapon, dropdown, queryset=Items.obj.filter(character).filter(offense)
* pacifist system, value in battle model, code in battlestack
* kill type count belongs to account, store it in player.models.Config, use throughs
* rename 'playing_toon' to 'playing_character'
* The (user|character)_is blocks are not DRY
