import time
import random
from strahd_battle_exposition import *
from strahd_battle_player_functions import *
from strahd_battle_strahd_functions import *
from prompts import ask_for_name, ask_for_class



#----------------------------BASIC GAMEPLAY MECHANIC DETIALS------------------------------


#strahd attributes
STRAHD_MAX_HP = 40
strahd_hp = 40
STRAHD_AC = 16
STRAHD_ATTACK_MOD = 9
strahd_last_move = ""
strahd_stunned = False

#battle counters or other details
turn_count = 0
strahd_initiative = random.randint(1,20)
strahd_last_move = ""

#list of class options for validating user input
class_options = ("fighter", "caster", "monk")

#fighter class details
FIGHTER_ATTRIBUTES = {"CLASS": "Fighter",
  "MAX HP": 30,
  "AC": 20,
  "ATTACK MOD": 9,
  "NUM ATTACKS": 3,
  "DAMAGE DICE": 6,
  "MAX SPECIALS": 3
}

#caster class details
CASTER_ATTRIBUTES = {"CLASS": "Caster",
  "MAX HP": 25,
  "AC": 17,
  "ATTACK MOD": 8,
  "NUM ATTACKS": 2,
  "DAMAGE DICE": 8,
  "MAX SPECIALS": 2
}

#monk class details
MONK_ATTRIBUTES = {"CLASS": "Monk",
  "MAX HP": 25,
  "AC": 20,
  "ATTACK MOD": 9,
  "NUM ATTACKS": 5,
  "DAMAGE DICE": 4,
  "MAX SPECIALS": 3
}



#------------------------------------INTRO AND SETUP----------------------------------------

ascii_art.print()
intro_monologue.play()

player_name = ask_for_name().title()
classes.print()
player = ask_for_class(player_name)

conceit.print()

player_initiative = initiative_roll(competing_initiative=strahd_initiative)

#if player goes first, player goes on even turns, or turns where turn_count % 2 == 0.
#otherwise, player goes on odd turns, or turns where turn_count % 2 == 1.
#assign player_turn_mod accordingly.
if player_initiative > strahd_initiative:
  player_turn_mod = 0
else:
  player_turn_mod = 1



#------------------------------GAMEPLAY/TURN ALTERNATOR-------------------------------------


while player.current_hp > 0 and strahd_hp > 0: #While both Strahd and player are up and fighting
  # If it's currently player's turn:
  if turn_count % 2 == player_turn_mod:
    while True: #loop to capture invalid choices (miskeys or attempts to SPECIAL too many times)
      player_move = input("What would you like to do? ATTACK or SPECIAL? ")

      if player_move.lower() == "attack":
        strahd_hp -= player.attack_action(competing_ac=STRAHD_AC)
        strahd_status(current_hp=strahd_hp,max_hp=STRAHD_MAX_HP)
        print()
        break

      elif player_move.lower() == "special":
        if player.current_specials <= 0:
          print("No specials left!")
        else:
          results = player.special(competing_ac=STRAHD_AC)
          strahd_hp -= results.damage
          strahd_stunned = results.strahd_stunned
          break

      else:
        print("That's not in your moveset.")
  # If it's currently Strahd's turn
  else:
    if strahd_stunned == False:
        strahd_turn = strahd_attack_action(competing_ac=player.armor_class)
        player.take_damage(strahd_turn[0])
        strahd_last_move = strahd_turn[1]
    else:
        print("Strahd is stunned! He strains to lunge at you but he's too stiff to move.")
        print()
        strahd_stunned = False # Remove stunned status after one turn

    if player.current_hp > 0:
      print(f"Your remaining hp: {player.current_hp}.")

  turn_count += 1 #increment turn count

ending_sequence(p_hp=player.current_hp,
                last_move=strahd_last_move,
                p_name=player_name,
                p_class=player.class_name)