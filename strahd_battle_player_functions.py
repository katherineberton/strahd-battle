#move player action functions here once I figure out how to get around the undefined variables
#possibly will have to pare down these functions so they don't relate to variables in the main file?
#maybe databases will help?
#maybe passing in variables as parameters will help instead of trying to use global ones?

#list of problem items:
#initiative_roll, because it compares to strahd's initiative roll
#attack_roll, because it needs player_attack_mod
#attack_action, because it needs player_num_attacks, strahd_ac, player_damage_dice and, indirectly, player_attack_mod since attack_roll is called as well
#stunning_strike, because it needs strahd_ac