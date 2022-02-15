from fileinput import filename
import random
import time

#ask simon if it's poor form to have a function that needs so many parameters



#-----------------------------------INTRODUCTIONS AND INFORMATION------------------------------------------


#strahd_ascii
def strahd_ascii(filename):
  for line in open(filename):
    print(line, end="")


#strahd intro
def strahd_monologue():
  """Strahd intro monologue"""
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


#game explanation
def conceit():
  """explains the stakes of the fight"""
  print("The time has come! This is your last chance to escape Barovia and go home!")
  print("He's strong, but so are you. You can do this.")
  print("If you defeat him, the mists will dissipate, and you'll be free.")
  print()


#class options
def describe_classes():
  
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
  print("Attack: punch five times in a flurry of blows (unlimited).")
  print("Special: paralyze Strahd for a turn with a Stunning Strike (three times max).")
  print("")


#strahd battle weariness
def strahd_status(current_hp, max_hp):
  """lets the player know how roughed up Strahd looks by his remaining HP"""

  if current_hp/max_hp > .75:
    pass
  elif .5 < current_hp/max_hp <= .75:
    print("Strahd seems enraged.")
  elif .25 <= current_hp/max_hp <= .5:
    print("You can see fear in Strahd's eyes.")
  elif current_hp <= 0:
    pass
  else:
    print("Strahd can barely stand. Finish him!")



#--------------------------------------POST BATTLE OUTROS----------------------------------------


#player win outro
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


#strahd final blow claw outro
def strahd_wins_claw(p_name, p_class):
  """describes player's final moments with a claw swipe as Strahd's final action"""

  print("Strahd is just too powerful. He pins you to the floor, his claws at your neck, and he leans in close.")
  time.sleep(2)
  print(f"'I have ruled this land for centuries, {p_name}. I have quashed dozens of insurrections and prevented hundreds more.'")
  time.sleep(2)
  print(f"'Imagine the arrogance to think you, a {p_class}, were somehow different from the rest.'")
  time.sleep(2)
  print("'No matter. You think since your demise is imminent, you are free, but you are not. The mists don't just cage the living. They cage everything.'")
  time.sleep(2)
  print("'Now your soul can spend eternity trapped in this place like me!'")


#strahd final blow bite outro
def strahd_wins_bite(p_name, p_class):
  """describes player's final moments with a bite as Strahd's final action"""

  print("Strahd is just too strong. He pins you to the floor, his claws at your neck, and he leans in close.")
  time.sleep(2)
  print(f"'I have ruled this land for centuries, {p_name}. I have quashed dozens of insurrections and prevented hundreds more.'")
  time.sleep(2)
  print("'But you... you are the only one who has come this far.'")
  time.sleep(2)
  print(f"'Despite our differences, I think you can still serve a purpose. You have some power, {p_class}. Watch me make you even more powerful.'")
  time.sleep(2)
  print("His teeth sink in to your neck. His skin is cold, but your blood starts turning it warm.")


#tests conditions at end of game and plays the appropriate outro
def ending_sequence(p_hp, last_move, p_name, p_class):
  """if player wins then describes Strahd's final moments. if Strahd wins, then describes player's final moment based on strahd's last move."""

  if p_hp <= 0: #if player lost
    if last_move == "bite":
      strahd_wins_bite(p_name, p_class)
    elif last_move == "claw":
      strahd_wins_claw(p_name, p_class)
  else:
    player_wins()