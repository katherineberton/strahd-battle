import random
import time



#--------------------------------------STRAHD COMBAT ACTIONS-----------------------------------------


#strahd attack 1: bite
def strahd_bite(attack_mod, competing_ac):
  """rolls a d20 and adds 12 to hit. rolls 2d6 for damage. Returns damage and updates Strahd's last move."""

  bite_damage = 0

  if random.randint(1,20) + attack_mod >= competing_ac: #if Strahd hits

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


#strahd attack 2: claw
def strahd_claws(attack_mod, competing_ac):
  """Rolls a d20 plus 12 to hit. Rolls a d4 + 2 for damage. Repeats. Returns damage and updates Strahd's last move."""

  print("Strahd extends his claws and rears back with both hands.")

  claw_damage_accumulator = 0
  attack_counter = 0

  #while loop to capture two attacks, one from each hand
  while attack_counter < 2:
    
    attack_to_hit = random.randint(1,20) + attack_mod

    if attack_to_hit >= competing_ac: #if Strahd hits

      print("Strahd slashes at you with a claw.")
      damage = random.randint(1,4) + 2
      claw_damage_accumulator += damage

    else:

      print("You are just out of his reach!")
    
    attack_counter += 1
  
  print(f"Strahd did {claw_damage_accumulator} damage.")
  return (claw_damage_accumulator, "claw")


#strahd attack randomizer
def strahd_attack_action(attack_mod, competing_ac):
  """randomizes Strahd's claw attack or bite attack"""

  if random.randint(1,2) == 1:
    strahd_attack = strahd_bite(attack_mod, competing_ac)
  else:
    strahd_attack = strahd_claws(attack_mod, competing_ac)
  
  print()
  time.sleep(1)
  return strahd_attack