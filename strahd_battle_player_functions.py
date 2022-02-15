import random
import time

#ask simon if it's poor form to have a function that needs so many parameters



#--------------------------------------PLAYER SETUP------------------------------------------


#get player name
def ask_for_name():

  name = input("What is your name? ")
  print()
  return name


#get player class
def ask_for_class(options):
  """prompts the player to pick a class."""

  #while True catch for invalid answers, repeats choice back
  while True:
    class_choice = input("Are you a FIGHTER, a CASTER, or a MONK? ")
    if class_choice.lower() not in options:
      print("That was not on the list. Are you a FIGHTER, a CASTER, or a MONK?")
    else:
      break
  print(f"Great, a powerful {class_choice.lower()}.")
  print()

  return class_choice


def initiative_roll(competing_initiative):
  """prompts the player with "input" to roll a d20 to see who goes first."""

  #says to press ENTER but any key stroke will work
  input("Roll your D20 to see who goes first by pressing ENTER. ")
  initiative = random.randint(1,20)

  print(f"Result: {initiative}.")

  #while True loop to catch the condition of Strahd initiative == player initiative
  while True:
    if initiative == competing_initiative:
      input("Roll again.")
      initiative = random.randint(1,20)
    else:
      if initiative > competing_initiative:
        print("You caught him off guard!")
      else:
        print("He is just too fast!")
      break
  print()

  return initiative



#---------------------------------------------PLAYER ATTACK ACTIONS---------------------------------------


#player's roll to hit
def attack_roll(attack_mod):
  """prompts the player to roll a d20 to see if their attack hits. Adds the player's attack modifier to the resultant roll. Returns the roll."""

  input(f"Roll your D20 to try to hit by pressing ENTER. ")

  to_hit = random.randint(1,20) + attack_mod
  print(f"Result: {to_hit}")
  return to_hit


#player's full attack action
def attack_action(num_attacks, attack_mod, competing_ac, damage_dice):
  """attacks based on player's attack stats - number of attacks, attack mod, damage dice. Accumulates and returns damage dealt."""

  attack_damage_accumulator = 0
  attack_counter = 0

  while attack_counter < num_attacks:
    if attack_roll(attack_mod) >= competing_ac:
      print("You hit!")
      damage = random.randint(1,damage_dice)
      attack_damage_accumulator += damage
    else:
      print("Ouch, you missed.")
    attack_counter += 1

  print(f"You did {attack_damage_accumulator} damage.")
  time.sleep(1)
  return attack_damage_accumulator



#--------------------------------------PLAYER SPECIAL ACTIONS-----------------------------------


#fighter special
def second_wind():
  """this is the fighter's special move. returns hp gained"""

  input("Roll a D4 by pressing ENTER. ")
  hp_gain = random.randint(1,4) + 1

  print(f"HP gained: {hp_gain}")
  print()
  time.sleep(1)
  return hp_gain


#caster special
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


#monk special
def stunning_strike(attack_mod, competing_ac):
  """this is the monk's special move. does a single attack with a larger than normal amount of damage and stuns on a hit.
  
  this function returns a tuple with damage dealt and stunned status."""
  
  if attack_roll(attack_mod) >= competing_ac:
    damage = random.randint(1,10)
    print("You hit!")
    print(f"You did {damage} damage.")
    print()
    return (damage, True)
  else:
    print("Your punch bounces off his armor and Strahd shakes off the stun.")
    print()
    return (0, False)


