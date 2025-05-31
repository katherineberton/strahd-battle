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
  strahd: Strahd

  def __init__(self):
    self.strahd = Strahd(name="Strahd")
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
  
  def report_strahd_status(self):
    if self.strahd.current_hp <= 0:
      return
    
    percent_left = self.strahd.current_hp/self.strahd.max_hp
    if percent_left > .75:
      pass
    elif .5 < percent_left <= .75:
      print("Strahd seems enraged.")
    elif .25 <= percent_left <= .5:
      print("You can see fear in Strahd's eyes.")
    else:
      print("Strahd can barely stand. Finish him!")

  def increment_turn(self):
    self.turn_count += 1

  def intro(self):
    ascii_art.print()
    intro_monologue.play()
    self.set_player()
    conceit.print()
    self.set_player_initiative()


  def outro(self):
    ending_sequence(player=self.player, last_move=self.strahd.last_move)

  def turn_alternator(self):
    while self.player.current_hp > 0 and self.strahd.current_hp > 0: #While both Strahd and player are up and fighting
      if self.is_players_turn():
        self.player_move()
      else:
        self.strahd_move()
      self.increment_turn()

  def player_move(self):
    while True: #loop to capture invalid choices (miskeys or attempts to SPECIAL too many times)
      player_move = input("What would you like to do? ATTACK or SPECIAL? ")

      if player_move.lower() == "attack":
        self.strahd.take_damage(self.player.attack_action(competing_ac=self.strahd.armor_class))
        self.report_strahd_status()
        print()
        break

      elif player_move.lower() == "special":
        if self.player.current_specials <= 0:
          print("No specials left!")
        else:
          results = self.player.special(competing_ac=self.strahd.armor_class)
          self.strahd.take_damage(results.damage)
          self.strahd.stunned = results.stunned
          self.report_strahd_status()
          break

      else:
        print("That's not in your moveset.")

  def strahd_move(self):
    if self.strahd.stunned == False:
      self.player.take_damage(self.strahd.attack(competing_ac=self.player.armor_class))
    else:
      print("Strahd is stunned! He strains to lunge at you but he's too stiff to move.")
      print()
      self.strahd.stunned = False # Remove stunned status after one turn

    if self.player.current_hp > 0:
      print(f"Your remaining hp: {self.player.current_hp}.")

  def play(self):
    self.intro()
    self.turn_alternator()
    self.outro()


game = Gameplay()
game.play()
