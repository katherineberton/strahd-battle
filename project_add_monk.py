import time
import random
from strahd_battle_exposition import strahd_monologue, conceit, player_wins, strahd_status, strahd_wins_claw, strahd_wins_bite

#-----------------------------------WISH LIST----------------------------------------

#fine tune hp and dmg output
#add an npc ally
#change all remaining functions so that they pass in global variables when called to avoid undefined variable errors
#add a function called player_hits and strahd_hits for better english readability. or just hits, or something.

#----------------------------FUNCTIONS - exposition----------------------------------

def ending_sequence():
  """if player wins then describes Strahd's final moments. if Strahd wins, then describes player's final moment based on strahd's last move."""

  if player_hp <= 0:
    if strahd_last_move == "bite":
      strahd_wins_bite(p_name=player_name, p_class=player_class)
    else:
      strahd_wins_claw(p_name=player_name, p_class=player_class)
  else:
    player_wins()

#----------------------------FUNCTIONS - player actions---------------------------------


def ask_for_name():

  name = input("What is your name? ")
  print()
  return name
  

def ask_for_class():
  """describes the three class options and prompts the player to pick one. Contains a while loop catch for invalid answers."""

  #explains options to player:
  print("What's your specialty? Options:")
  print()
  print("FIGHTER")
  print("Attack: swing three times with your sword (unlimited).")
  print("Special: use Second Wind to gain HP (three times max).")
  print()
  print("CASTER")
  print("Attack: fire two Eldritch Blasts (unlimited).")
  print("Special: envelop Strahd in sunlight with Dawn (twice max).")
  print()
  print("MONK")
  print("Attack: punch five times in a flurry of blows.")
  print("Special: paralyze Strahd for a turn with a Stunning Strike (three times max).")
  print("")

  #prompts player to choose one with a while True catch for invalid answers, repeats it back to them.
  while True:
    class_choice = input("Are you a FIGHTER, a CASTER, or a MONK? ")
    if class_choice.lower() not in ["fighter", "caster", "monk"]:
      print("That was not on the list. Are you a FIGHTER, a CASTER, or a MONK?")
    else:
      break
  print(f"Great, a powerful {class_choice.lower()}.")
  print()

  return class_choice


def initiative_roll():
  """prompts the player with "input" to roll a d20 to see who goes first."""

  #says to press ENTER but any key stroke will work
  input("Roll your D20 to see who goes first by pressing ENTER. ")
  initiative = random.randint(1,20)

  print(f"Result: {initiative}.")

  #while True loop to catch the condition of Strahd initiative == player initiative
  while True:
    if initiative == strahd_initiative:
      input("Roll again.")
      initiative = random.randint(1,20)
    else:
      if initiative > strahd_initiative:
        print("You caught him off guard!")
      else:
        print("He is just too fast!")
      break
  print()

  return initiative


def attack_roll():
  """prompts the player to roll a d20 to see if their attack hits. Adds the player's attack modifier to the resultant roll. Returns the roll."""

  input(f"Roll your D20 to try to hit by pressing ENTER. ")

  to_hit = random.randint(1,20) + PLAYER_ATTACK_MOD
  print(f"Result: {to_hit}")
  return to_hit


def attack_action():
  """attacks based on player's attack stats - number of attacks, attack mod, damage dice. Accumulates and returns damage dealt."""

  attack_damage_accumulator = 0
  attack_counter = 0

  while attack_counter < PLAYER_NUM_ATTACKS:
    if attack_roll() >= STRAHD_AC:
      print("You hit!")
      damage = random.randint(1,PLAYER_DAMAGE_DICE)
      attack_damage_accumulator += damage
    else:
      print("Ouch, you missed.")
    attack_counter += 1

  print(f"You did {attack_damage_accumulator} damage.")
  time.sleep(1)
  return attack_damage_accumulator

def second_wind():
  """this is the fighter's special move. returns hp gained"""

  input("Roll a D4 by pressing ENTER. ")
  hp_gain = random.randint(1,4) + 1

  print(f"HP gained: {hp_gain}")
  print()
  time.sleep(1)
  return hp_gain


def dawn():
  """this is the caster's special move. describes the spell and accumulates and returns damage"""

  print("A massive cylinder of searing light appears around Strahd.")
  input("Press ENTER to roll for damage. ")
  dawn_damage = 0
  i = 0

  while i < 4:
    dawn_damage += random.randint(1,4)
    i += 1

  print(f"You did {dawn_damage} damage.")
  print()
  time.sleep(1)
  return dawn_damage


def stunning_strike():
  """this is the monk's special move. does a single attack with a larger than normal amount of damage and returns stunned status to Strahd."""
  
  if attack_roll() >= STRAHD_AC:
    print("You hit!")
    print()
    damage = random.randint(1,10)
    return (damage, True)
  else:
    print("Your punch bounces off his armor and Strahd shakes off the stun.")
    print()
    return (0, False)

#----------------------------FUNCTIONS - Strahd actions---------------------------------

def strahd_bite():
  """rolls a d20 and adds 12 to hit. rolls 2d6 for damage. Returns damage and updates Strahd's last move."""

  bite_damage = 0

  if random.randint(1,20) + STRAHD_ATTACK_MOD >= PLAYER_AC: #if Strahd hits

    print("Strahd sinks his fangs into you!")
    
    #roll 2d6
    i = 0
    while i < 2:
      bite_damage += random.randint(1,6)
      i += 1
    
    print(f"Strahd did {bite_damage} damage.")

  else:
    print("Strahd lunges for your exposed neck but misses!")
  
  return (bite_damage, "bite")


def strahd_claws():
  """Rolls a d20 plus 12 to hit. Rolls a d4 + 2 for damage. Repeats. Returns damage and updates Strahd's last move."""

  print("Strahd extends his claws and rears back with both hands.")

  claw_damage_accumulator = 0
  attack_counter = 0

  #while loop to capture two attacks, one from each hand
  while attack_counter < 2:
    
    attack_to_hit = random.randint(1,20) + STRAHD_ATTACK_MOD

    if attack_to_hit >= PLAYER_AC: #if Strahd hits

      print("Strahd slashes at you with a claw.")
      damage = random.randint(1,4) + 2
      claw_damage_accumulator += damage

    else:

      print("You are just out of his reach!")
    
    attack_counter += 1
  
  print(f"Strahd did {claw_damage_accumulator} damage.")
  return (claw_damage_accumulator, "claw")


def strahd_attack_action():
  """randomizes Strahd's claw attack or bite attack"""

  if random.randint(1,2) == 1:
    strahd_attack = strahd_bite()
  else:
    strahd_attack = strahd_claws()
  
  print()
  time.sleep(1)
  return strahd_attack


#----------------------------DECLARING GLOBAL VARIABLES---------------------------------


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

FIGHTER_ATTRIBUTES = {"CLASS": "Fighter",
  "MAX HP": 30,
  "AC": 20,
  "ATTACK MOD": 9,
  "NUM ATTACKS": 3,
  "DAMAGE DICE": 6,
  "MAX SPECIALS": 3
}

CASTER_ATTRIBUTES = {"CLASS": "Caster",
  "MAX HP": 25,
  "AC": 17,
  "ATTACK MOD": 8,
  "NUM ATTACKS": 2,
  "DAMAGE DICE": 8,
  "MAX SPECIALS": 2
}

MONK_ATTRIBUTES = {"CLASS": "Monk",
  "MAX HP": 25,
  "AC": 20,
  "ATTACK MOD": 9,
  "NUM ATTACKS": 5,
  "DAMAGE DICE": 4,
  "MAX SPECIALS": 3
}


#---------------------------PLAYER INPUT AND CONDITIONALS-------------------------------


strahd_monologue()

#prompting for player's name after printing Strahd's opening monologue for style reasons
player_name = ask_for_name().title()
player_class = ask_for_class()

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

player_initiative = initiative_roll()

#if player goes first, player goes on even turns, or turns where turn_count % 2 == 0, meaning player_turn_mod = 0. otherwise, player goes on odd turns, or turns where turn_count % 2 == 1, so player_turn_mod = 1

if player_initiative > strahd_initiative:
  player_turn_mod = 0
else:
  player_turn_mod = 1

#gameplay/turn alternator

while player_hp > 0 and strahd_hp > 0: #while both strahd and player are up and fighting

  if turn_count % 2 == player_turn_mod: #if it's currently player's turn:

    while True: #loop to capture invalid choices (miskeys or attempts to SPECIAL too many times)
      player_choice = input("What would you like to do? ATTACK or SPECIAL? ")

      if player_choice.lower() == "attack": #ATTACK is a valid choice always, breaks the loop
        strahd_hp -= attack_action()
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
            monk_attack = stunning_strike()
            strahd_hp -= monk_attack[0]
            strahd_stunned = monk_attack[1]
          player_special_count -= 1
          break

      else:
        print("That's not in your moveset.")

  else: #if it's currently strahd's turn

    if strahd_stunned == False: #if strahd is not currently stunned, proceed with his attack action
        strahd_turn = strahd_attack_action()
        player_hp -= strahd_turn[0] #reduce player hp by whatever strahd attack action returns
        strahd_last_move = strahd_turn[1] #update strahd's last move to either "claw" or "bite" depending on which action he performed
    else:
        print("Strahd is stunned!")
        print()
        strahd_stunned = False #remove stunned status at end of turn

    if player_hp > 0: #if player's hp has not been reduced beyond 0
      print(f"Your remaining hp: {player_hp}.")

  turn_count += 1 #increment turn count

ending_sequence()