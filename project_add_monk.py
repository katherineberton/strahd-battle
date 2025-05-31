import time
import random
from strahd_battle_exposition import *
from strahd_battle_player_functions import *
from strahd_battle_strahd_functions import *
from prompts import ask_for_name, ask_for_class, initiative_roll
from characters import Strahd



#----------------------------BASIC GAMEPLAY MECHANIC DETIALS------------------------------




#battle counters or other details
turn_count = 0
strahd_initiative = random.randint(1,20)
strahd_last_move = ""


#------------------------------------INTRO AND SETUP----------------------------------------

# ascii_art.print()
# intro_monologue.play()

player_name = ask_for_name().title()
# classes.print()
player = ask_for_class(player_name)

conceit.print()

strahd = Strahd(name="Strahd")
player_initiative = initiative_roll(competing_initiative=strahd_initiative)

#if player goes first, player goes on even turns, or turns where turn_count % 2 == 0.
#otherwise, player goes on odd turns, or turns where turn_count % 2 == 1.
#assign player_turn_mod accordingly.
if player_initiative > strahd_initiative:
  player_turn_mod = 0
else:
  player_turn_mod = 1



#------------------------------GAMEPLAY/TURN ALTERNATOR-------------------------------------


while player.current_hp > 0 and strahd.current_hp > 0: #While both Strahd and player are up and fighting
  # If it's currently player's turn:
  if turn_count % 2 == player_turn_mod:
    while True: #loop to capture invalid choices (miskeys or attempts to SPECIAL too many times)
      player_move = input("What would you like to do? ATTACK or SPECIAL? ")

      if player_move.lower() == "attack":
        strahd.take_damage(player.attack_action(competing_ac=strahd.armor_class))
        strahd_status(current_hp=strahd.current_hp, max_hp=strahd.max_hp)
        print()
        break

      elif player_move.lower() == "special":
        if player.current_specials <= 0:
          print("No specials left!")
        else:
          results = player.special(competing_ac=strahd.armor_class)
          strahd.take_damage(results.damage)
          strahd.stunned = results.stunned
          break

      else:
        print("That's not in your moveset.")

  # If it's currently Strahd's turn
  else:
    if strahd.stunned == False:
        player.take_damage(strahd.attack(competing_ac=player.armor_class))
    else:
        print("Strahd is stunned! He strains to lunge at you but he's too stiff to move.")
        print()
        strahd.stunned = False # Remove stunned status after one turn

    if player.current_hp > 0:
      print(f"Your remaining hp: {player.current_hp}.")

  turn_count += 1 #increment turn count

ending_sequence(p_hp=player.current_hp,
                last_move=strahd.last_move,
                p_name=player.name,
                p_class=player.class_name)