import time
from characters import  Fighter, Caster, Monk

class Exposition:
  name: str
  description: str
  lines: list[str]

  def __init__(self, name: str, lines: list[str], description: str = ''):
    self.name = name
    self.lines = lines
    self.description = description

  def play(self):
    line_idx = 0
    while line_idx < len(self.lines):
      print(self.lines[line_idx])
      time.sleep(2)
      line_idx += 1

  def print(self):
    for line in self.lines:
      print(line.rstrip('\n'))


ascii_art = Exposition(
  name='ascii_art',
  lines=open('assets/strahd_ascii.txt'),
  description="Strahd art"
)
intro_monologue = Exposition(
  name='intro_monologue',
  lines=[
    "\n'You.'",
    "'You have been a thorn in my side since you came to Barovia.'",
    "'I invited you into my home. I have been a gracious host. And despite this...'",
    "'You CONTINUE TO DEFY ME.'",
    "'You rebuff my extensions of grace, you disrupt local businesses, you upset my citizens, and you damage local ecosystems.'",
    "'I thought we could be useful to each other. It's clear that you are far more trouble than you're worth.'",
    "'Now die, and your soul will be mine forever.'",
    "Strahd lunges at you. \n----------------------------------------------------------------\n",
  ],
  description='Strahd airs his grievances'
)
conceit = Exposition(
  name="conceit",
  lines=[
    "The time has come! This is your last chance to escape Barovia and go home!",
    "He's strong, but so are you. You can do this.",
    "If you defeat him, the mists will dissipate, and you'll be free.",
    "",
  ],
  description="Describes the stakes of the fight"
)


def _get_describe_classes_lines():
  all_classes = [Fighter().details, Caster().details, Monk().details]
  lines = ["What's your specialty? Options:", ""]
  for player_class in all_classes:
    lines.append(f"{player_class.name}")
    lines.append(f"Attack: {player_class.attack}")
    lines.append(f"Special: {player_class.special}")
    lines.append("")
  return lines
classes = Exposition(
  name="classes",
  lines=_get_describe_classes_lines(),
  description="Describes the classes"
)
player_wins = Exposition(
  name="player_wins",
  lines=[
    "STRAHD FALLS TO THE GROUND.",
    "His claws twitch. His head lolls to the side.",
    "Suddenly...",
    "He bursts into a cloud of smoke. The smoke hangs in the air, lingering a moment... and it feels like it's looking at you.",
    "With haste, it moves for the door and fills the cracks and keyholes.",
    "Then it's gone.",
    "You look outside and for the first time in months you see... sunlight.",
  ],
  description="What player sees when they defeat Strahd and escape Barovia"
)

def _get_strahd_wins_bite_lines(player):
  return [
    "Strahd is just too strong. He pins you to the floor, his claws at your neck, and he leans in close.",
    f"'I have ruled this land for centuries, {player.name}. I have quashed dozens of insurrections and prevented hundreds more.'",
    "'But you... you are the only one who has come this far.'",
    f"'Despite our differences, I think you can still serve a purpose. You have some power, {player.class_name}. Watch me make you even more powerful.'",
    "His teeth sink in to your neck. His skin is cold, but your blood starts turning it warm.",
  ]
strahd_wins_bite = Exposition(
  name="strahd_wins_bite",
  lines=_get_strahd_wins_bite_lines(),
  description="What player sees when Strahd wins with a bite"
)

def _get_strahd_wins_claw_lines(player):
  return [
    "Strahd is just too powerful. He pins you to the floor, his claws at your neck, and he leans in close.",
    f"'I have ruled this land for centuries, {player.name}. I have quashed dozens of insurrections and prevented hundreds more.'",
    "'Imagine the arrogance to think you, a {player.class_name}, were somehow different from the rest.'",
    "'No matter. You think since your demise is imminent, you are free, but you are not. The mists don't just cage the living. They cage everything.'",
    "'Now your soul can spend eternity trapped in this place like me!'",
  ]
strahd_wins_claw = Exposition(
  name="strahd_wins_claw",
  lines=_get_strahd_wins_claw_lines(),
  description="What player sees when Strahd wins with a claw"
)

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
    player_wins.play()