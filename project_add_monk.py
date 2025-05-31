import random
from strahd_battle_exposition import *
from prompts import ask_for_name, ask_for_class, initiative_roll
from characters import Strahd, PlayerClass


class Gameplay:
  turn_count: int = 0
  
  strahd_initiative: int
  player_initiative: int
  player_turn_mod: int

  player: PlayerClass

  def __init__(self):
    self.strahd_initiative = random.randint(1,20)

  def get_player_initiative(self):
    self.player_initiative = initiative_roll(competing_initiative=self.strahd_initiative)

    # If player goes first, player goes on even turns, or turns where turn_count % 2 == 0.
    # Otherwise, player goes on odd turns, or turns where turn_count % 2 == 1.
    self.player_turn_mod = 0 if self.player_initiative > self.strahd_initiative else 1

  def is_players_turn(self):
    return self.turn_count % 2 == self.player_turn_mod
  
  def increment_turn(self):
    self.turn_count += 1

  def intro(self):
    ascii_art.print()
    intro_monologue.play()



#------------------------------------INTRO AND SETUP----------------------------------------
game = Gameplay()

game.intro()

player_name = ask_for_name().title()
classes.print()
player = ask_for_class(player_name)

conceit.print()

game.get_player_initiative()
strahd = Strahd(name="Strahd")


#------------------------------GAMEPLAY/TURN ALTERNATOR-------------------------------------


while player.current_hp > 0 and strahd.current_hp > 0: #While both Strahd and player are up and fighting
  # If it's currently player's turn:
  if game.is_players_turn():
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

  game.increment_turn()

ending_sequence(player=player, last_move=strahd.last_move)