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

  def set_player(self):
    player_name = ask_for_name().title()
    classes.print()
    self.player = ask_for_class(player_name)

  def set_player_initiative(self):
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

game = Gameplay()
strahd = Strahd(name="Strahd")

game.intro()
game.set_player()
conceit.print()
game.set_player_initiative()

#------------------------------GAMEPLAY/TURN ALTERNATOR-------------------------------------

while game.player.current_hp > 0 and strahd.current_hp > 0: #While both Strahd and player are up and fighting
  # If it's currently player's turn:
  if game.is_players_turn():
    while True: #loop to capture invalid choices (miskeys or attempts to SPECIAL too many times)
      player_move = input("What would you like to do? ATTACK or SPECIAL? ")

      if player_move.lower() == "attack":
        strahd.take_damage(game.player.attack_action(competing_ac=strahd.armor_class))
        strahd_status(current_hp=strahd.current_hp, max_hp=strahd.max_hp)
        print()
        break

      elif player_move.lower() == "special":
        if game.player.current_specials <= 0:
          print("No specials left!")
        else:
          results = game.player.special(competing_ac=strahd.armor_class)
          strahd.take_damage(results.damage)
          strahd.stunned = results.stunned
          break

      else:
        print("That's not in your moveset.")

  # If it's currently Strahd's turn
  else:
    if strahd.stunned == False:
        game.player.take_damage(strahd.attack(competing_ac=game.player.armor_class))
    else:
        print("Strahd is stunned! He strains to lunge at you but he's too stiff to move.")
        print()
        strahd.stunned = False # Remove stunned status after one turn

    if game.player.current_hp > 0:
      print(f"Your remaining hp: {game.player.current_hp}.")

  game.increment_turn()

ending_sequence(player=game.player, last_move=strahd.last_move)