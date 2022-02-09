import time
import random

#----------------------------------TO DO LIST----------------------------------------

#fine tune hp and dmg output
#add an npc ally

#----------------------------FUNCTIONS - exposition----------------------------------

def strahd_monologue():
  """Strahd being dramatic"""
  print("'You.'")
  time.sleep(2)
  print("'You have been a thorn in my side since you came to Barovia.'")
  time.sleep(2)
  print("'I invited you into my home. I have been a gracious host. And despite this...'")
  time.sleep(2)
  print("'You CONTINUE TO DEFY ME.'")
  time.sleep(2)
  print("'You rebuff my extensions of grace, you disrupt local businesses, you upset my citizens, and you damage local ecosystems.'")
  time.sleep(2)
  print("'I thought we could be useful to each other. It's clear that you are far more trouble than you're worth.'")
  time.sleep(2)
  print("'Now die, and your soul will be mine forever.'")
  time.sleep(3)
  print("Strahd lunges at you.")
  print("----------------------------------------------------------------")
  print()

def conceit():
  """explains the stakes of the fight"""
  print("The time has come! This is your last chance to escape Barovia and go home!")
  print("He's strong, but so are you. You can do this.")
  print("If you defeat him, the mists will dissipate, and you'll be free.")
  print()

def strahd_status():
  """lets the player know how close they are to defeating Strahd by his remaining HP"""

  if strahd_hp/STRAHD_MAX_HP > .75:
    pass
  elif .5 < strahd_hp/STRAHD_MAX_HP <= .75:
    print("Strahd seems enraged.")
  elif .25 <= strahd_hp/STRAHD_MAX_HP <= .5:
    print("You can see fear in Strahd's eyes.")
  elif strahd_hp <= 0:
    pass
  else:
    print("Strahd can barely stand. Finish him!")

def player_wins():
  """describes Strahd's final moments"""

  print("STRAHD FALLS TO THE GROUND.")
  time.sleep(3)
  print("His claws twitch. His head lolls to the side.")
  time.sleep(2)
  print("Suddenly...")
  time.sleep(2)
  print("He bursts into a cloud of smoke. The smoke hangs in the air, lingering a moment... and it feels like it's looking at you.")
  time.sleep(2)
  print("With haste, it moves for the door and fills the cracks and keyholes.")
  time.sleep(2)
  print("Then it's gone.")
  time.sleep(3)
  print("You look outside and for the first time in months you see... sunlight.")

def strahd_wins_claw():
  """describes player's final moments with a claw swipe as Strahd's final action"""

  print("Strahd is just too powerful. He pins you to the floor, his claws at your neck, and he leans in close.")
  time.sleep(2)
  print(f"'I have ruled this land for centuries, {player_name}. I have quashed dozens of insurrections and prevented hundreds more.'")
  time.sleep(2)
  print(f"'Imagine the arrogance to think you, a {player_class}, were somehow different from the rest.'")
  time.sleep(2)
  print("'No matter. You think since your demise is imminent, you are free, but you are not. The mists don't just cage the living. They cage everything.'")
  time.sleep(2)
  print("'Now your soul can spend eternity trapped in this place like me!'")

def strahd_wins_bite():
  """describes player's final moments with a bite as Strahd's final action"""

  print("Strahd is just too strong. He pins you to the floor, his claws at your neck, and he leans in close.")
  time.sleep(2)
  print(f"'I have ruled this land for centuries, {player_name}. I have quashed dozens of insurrections and prevented hundreds more.'")
  time.sleep(2)
  print("'But you... you are the only one who has come this far.'")
  time.sleep(2)
  print(f"'Despite our differences, I think you can still serve a purpose. You have some power, {player_class}. Watch me make you even more powerful.'")
  time.sleep(2)
  print("His teeth sink in to your neck. His skin is cold, but your blood starts turning it warm.")

def ending_sequence():
  """if player wins then describes Strahd's final moments. if Strahd wins, then plays final moment based on strahd's last move."""

  if player_hp <= 0:
    if strahd_last_move == "bite":
      strahd_wins_bite()
    else:
      strahd_wins_claw()
  else:
    player_wins()


#----------------------------FUNCTIONS - player actions---------------------------------

def ask_for_name():
  name = input("What is your name? ")
  print()
  return name

def ask_for_class():
  """describes the three class options and prompts the player to pick one. Contains a while loop catch for invalid answers."""

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
  """prompts the player with "input" to roll a d20 to see who goes first(says enter but any key stroke would work). Contains a while loop catch for the roll being equal to Strahd's initative."""

  input("Roll your D20 to see who goes first by pressing ENTER. ")
  initiative = random.randint(1,20)

  print(f"Result: {initiative}.")

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
  """attacks based on player's attack stats - number of attacks, attack mod, damage dice"""

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
  """this is the monk's special move. does a small amount of damage and returns stunned status to Strahd."""
  
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
  """rolls a d20 and adds 12 to hit. rolls 2d6 for damage."""

  bite_damage = 0

  if random.randint(1,20) + 12 >= PLAYER_AC:
    print("Strahd sinks his fangs into you!")
    i = 0
    while i < 2:
      bite_damage += random.randint(1,6)
      i += 1
    print(f"Strahd did {bite_damage} damage.")
  else:
    print("Strahd lunges for your exposed neck but misses!")
  
  return (bite_damage, "bite")

def strahd_claws():
  """Rolls a d20 plus 12 to hit. Rolls a d4 + 2 for damage. Repeats."""
  print("Strahd extends his claws and rears back with both hands.")

  claw_damage_accumulator = 0
  attack_counter = 0

  while attack_counter < 2:
    attack_to_hit = random.randint(1,20) + STRAHD_ATTACK_MOD
    if attack_to_hit >= PLAYER_AC:
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

#declaring a variable to make turn count identifiers more streamlined. if player goes first, player goes on even turns, or turns where turn_count % 2 == 0, meaning player_turn_mod = 0. otherwise, player goes on odd turns, or turns where turn_count % 2 == 1, so player_turn_mod = 1
if player_initiative > strahd_initiative:
  player_turn_mod = 0
else:
  player_turn_mod = 1

while player_hp > 0 and strahd_hp > 0: #while both strahd and player are up and fighting
  if turn_count % 2 == player_turn_mod: #if turn count mod 2 matches player turn count mod
    #player turn
    while True: #loop to capture no more specials or invalid choices
      player_choice = input("What would you like to do? ATTACK or SPECIAL? ")
      if player_choice.lower() == "attack": #attack is a valid choice always, breaks the loop
        strahd_hp -= attack_action()
        strahd_status()
        print()
        break
      elif player_choice.lower() == "special":
        if player_special_count <= 0: #if the player can't use any more specials, does not break the loop, asks again
          print("No specials left!")
        else: #if player DOES have more specials left, carries out special move and breaks the loop
          if player_class.title() == FIGHTER_ATTRIBUTES["CLASS"]: #if player chose fighter
            player_hp += second_wind()
          elif player_class.title() == CASTER_ATTRIBUTES["CLASS"]: #if player chose caster
            strahd_hp -= dawn()
            strahd_status()
            print()
          elif player_class.title() == MONK_ATTRIBUTES["CLASS"]: #if player chose monk
            monk_attack = stunning_strike()
            strahd_hp -= monk_attack[0]
            strahd_stunned = monk_attack[1]
          player_special_count -= 1
          break
      else:
        print("That's not in your moveset.")
  else:
    #strahd turn
    if strahd_stunned == False:
        strahd_turn = strahd_attack_action()
        player_hp -= strahd_turn[0] #reduce player hp by whatever strahd attack action returns
        strahd_last_move = strahd_turn[1] #update strahd's last move to either "claw" or "bite" depending on which action he performed
    else:
        print("Strahd is stunned!")
        print()
        strahd_stunned = False
    if player_hp > 0:
      print(f"Your remaining hp: {player_hp}.")
  turn_count += 1

ending_sequence()