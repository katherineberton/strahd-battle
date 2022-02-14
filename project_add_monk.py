import time
import random
from strahd_battle_exposition import *
from strahd_battle_player_functions import *
from strahd_battle_strahd_functions import *



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

strahd_ascii('strahd_ascii.txt')
strahd_monologue()

#prompting for player's name after printing Strahd's opening monologue for style reasons
player_name = ask_for_name().title()
describe_classes()
player_class = ask_for_class(options=class_options)

#declares other attributes based on the player's class choice
if player_class.lower() == FIGHTER_ATTRIBUTES["CLASS"].lower():
  player_hp = FIGHTER_ATTRIBUTES["MAX HP"]
  PLAYER_AC = FIGHTER_ATTRIBUTES["AC"]
  PLAYER_ATTACK_MOD = FIGHTER_ATTRIBUTES["ATTACK MOD"]
  PLAYER_NUM_ATTACKS = FIGHTER_ATTRIBUTES["NUM ATTACKS"]
  PLAYER_DAMAGE_DICE = FIGHTER_ATTRIBUTES["DAMAGE DICE"]
  player_special_count = FIGHTER_ATTRIBUTES["MAX SPECIALS"]
elif player_class.lower() == CASTER_ATTRIBUTES["CLASS"].lower():
  player_hp = CASTER_ATTRIBUTES["MAX HP"]
  PLAYER_AC = CASTER_ATTRIBUTES["AC"]
  PLAYER_ATTACK_MOD = CASTER_ATTRIBUTES["ATTACK MOD"]
  PLAYER_NUM_ATTACKS = CASTER_ATTRIBUTES["NUM ATTACKS"]
  PLAYER_DAMAGE_DICE = CASTER_ATTRIBUTES["DAMAGE DICE"]
  player_special_count = CASTER_ATTRIBUTES["MAX SPECIALS"]
elif player_class.lower() == MONK_ATTRIBUTES["CLASS"].lower():
  player_hp = MONK_ATTRIBUTES["MAX HP"]
  PLAYER_AC = MONK_ATTRIBUTES["AC"]
  PLAYER_ATTACK_MOD = MONK_ATTRIBUTES["ATTACK MOD"]
  PLAYER_NUM_ATTACKS = MONK_ATTRIBUTES["NUM ATTACKS"]
  PLAYER_DAMAGE_DICE = MONK_ATTRIBUTES["DAMAGE DICE"]
  player_special_count = MONK_ATTRIBUTES["MAX SPECIALS"]

conceit()

player_initiative = initiative_roll(competing_initiative=strahd_initiative)

#if player goes first, player goes on even turns, or turns where turn_count % 2 == 0.
#otherwise, player goes on odd turns, or turns where turn_count % 2 == 1.
#assign player_turn_mod accordingly.
if player_initiative > strahd_initiative:
  player_turn_mod = 0
else:
  player_turn_mod = 1



#------------------------------GAMEPLAY/TURN ALTERNATOR-------------------------------------


while player_hp > 0 and strahd_hp > 0: #while both strahd and player are up and fighting

  if turn_count % 2 == player_turn_mod: #if it's currently player's turn:

    while True: #loop to capture invalid choices (miskeys or attempts to SPECIAL too many times)
      player_choice = input("What would you like to do? ATTACK or SPECIAL? ")

      if player_choice.lower() == "attack": #ATTACK is a valid choice always, breaks the loop
        strahd_hp -= attack_action(num_attacks=PLAYER_NUM_ATTACKS,
                                   attack_mod=PLAYER_ATTACK_MOD,
                                   competing_ac=STRAHD_AC,
                                   damage_dice=PLAYER_DAMAGE_DICE)
        strahd_status(current_hp=strahd_hp,max_hp=STRAHD_MAX_HP)
        print()
        break

      elif player_choice.lower() == "special":
        if player_special_count <= 0: #if the player can't use any more specials, does not break the loop, asks again
          print("No specials left!")
        else: #if player DOES have more specials left, carries out special move and breaks the loop
          if player_class.title() == FIGHTER_ATTRIBUTES["CLASS"]: #if player chose fighter, use second wind
            player_hp += second_wind()
          elif player_class.title() == CASTER_ATTRIBUTES["CLASS"]: #if player chose caster, use dawn
            strahd_hp -= dawn()
            strahd_status(current_hp=strahd_hp,max_hp=STRAHD_MAX_HP)
            print()
          elif player_class.title() == MONK_ATTRIBUTES["CLASS"]: #if player chose monk, use stunning strike
            monk_attack = stunning_strike(attack_mod=PLAYER_ATTACK_MOD, competing_ac=STRAHD_AC)
            strahd_hp -= monk_attack[0]
            strahd_stunned = monk_attack[1]
          player_special_count -= 1
          break

      else:
        print("That's not in your moveset.")

  else: #if it's currently strahd's turn

    if strahd_stunned == False: #if strahd is not currently stunned, proceed with his attack action
        strahd_turn = strahd_attack_action(attack_mod=STRAHD_ATTACK_MOD, competing_ac=PLAYER_AC)
        player_hp -= strahd_turn[0] #reduce player hp by whatever strahd attack action returns
        strahd_last_move = strahd_turn[1] #update strahd's last move to either "claw" or "bite" depending on which action he performed
    else:
        print("Strahd is stunned!")
        print()
        strahd_stunned = False #remove stunned status at end of turn

    if player_hp > 0: #if player's hp has not been reduced beyond 0
      print(f"Your remaining hp: {player_hp}.")

  turn_count += 1 #increment turn count

ending_sequence(p_hp=player_hp,
                last_move=strahd_last_move,
                p_name=player_name,
                p_class=player_class)