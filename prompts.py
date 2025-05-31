from characters import Fighter, Caster, Monk
from strahd_battle_exposition import fighter_ascii, caster_ascii, monk_ascii
import random
import time

def ask_for_name():
  name = input("What is your name? ")
  print()
  return name

text_to_class_map = {
  "fighter": {"player_class": Fighter, "ascii": fighter_ascii},
  "caster": {"player_class": Caster, "ascii": caster_ascii},
  "monk": {"player_class": Monk, "ascii": monk_ascii},
}

def ask_for_class(player_name):
  """prompts the player to pick a class."""

  #while True catch for invalid answers, repeats choice back
  while True:
    class_choice = input("Are you a FIGHTER, a CASTER, or a MONK? ")
    if class_choice.lower() not in text_to_class_map:
      print("That was not on the list. Are you a FIGHTER, a CASTER, or a MONK?")
    else:
      selected_class = text_to_class_map[class_choice.lower()]
      break
  print(f"Great, a powerful {class_choice.lower()}.")
  time.sleep(1)
  selected_class["ascii"].print()
  time.sleep(1)
  print()

  return selected_class["player_class"](name=player_name)

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