DJGE
====

### TODO
* Make it possible to link multiple mobile.categories to a single world.location so we can spawn multiple types of combatants during random encounters.
* Charecter/equip weapon, dropdown, queryset=Items.obj.filter(character).filter(offense)
* pacifist system, value in battle model, code in battlestack
* kill type count belongs to account, store it in player.models.Config, use throughs
* rename 'playing_toon' to 'playing_character'
* I can probably replace "Combatant" with "NPC" because most (if not all) of the methods would apply to nonhostiles
* Convert Move() to a TemplateView but keep Triage the way it is. 
    * Move() needs some rewrite love anyway 
* Test making battle flow an updateview of the battle object; like /battle/ from the old builds. 
