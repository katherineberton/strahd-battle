from typing import Literal, NamedTuple
import random
import time

class MoveResult(NamedTuple):
    damage: int
    strahd_stunned: bool

class PlayerClass:
    class_name: str
    current_hp: int
    max_hp: int
    armor_class: int
    attack_mod: int
    attacks_per_attack_action: int
    damage_dice: Literal[4, 6, 8, 10, 12]
    max_specials: int
    current_specials: int

    def __init__(
        self,
        class_name,
        max_hp,
        armor_class,
        attack_mod,
        attacks_per_attack_action,
        damage_dice,
        max_specials
    ):
        self.class_name = class_name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.armor_class = armor_class
        self.attack_mod = attack_mod
        self.attacks_per_attack_action = attacks_per_attack_action
        self.damage_dice = damage_dice
        self.max_specials = max_specials
        self.current_specials = max_specials

    def attack_roll(self):
        input("Roll your d20 to try to hit by pressing ENTER. ")
        to_hit = random.randint(1,20) + self.attack_mod
        print(f"Result: {to_hit}")

        return to_hit

    def attack_action(self, competing_ac: int):
        attack_damage_accumulator = 0
        attack_counter = 0

        while attack_counter < self.attacks_per_attack_action:
            if self.attack_roll(self.attack_mod) >= competing_ac:
                print("You hit!")
                damage = random.randint(1,self.damage_dice)
                attack_damage_accumulator += damage
            else:
                print("Ouch, you missed.")
                attack_counter += 1

        print(f"You did {attack_damage_accumulator} damage.")
        time.sleep(1)
        return attack_damage_accumulator

    def take_damage(self, damage: int):
        self.current_hp -= damage

class Fighter(PlayerClass):
    def special(self):
        print("You use Second Wind!")
        input("Roll a D4 by pressing ENTER. ")
        hp_gain = random.randint(1,4) + 1

        print(f"HP gained: {hp_gain}")
        print()
        time.sleep(1)
        self.current_hp += hp_gain
        return MoveResult(damage=0, strahd_stunned=False)

class Caster(PlayerClass):
    def special(self):
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
        return MoveResult(damage=dawn_damage, status_effect=None)

class Monk(PlayerClass):
    def special(self, competing_ac: int):
        if self.attack_roll(self.attack_mod) >= competing_ac:
            damage = random.randint(1,10)
            print("You hit!")
            print(f"You did {damage} damage.")
            print()
            return MoveResult(damage=damage, strahd_stunned=True)
        else:
            print("Your punch bounces off his armor and Strahd shakes off the stun.")
            print()
            return MoveResult(damage=0, strahd_stunned=False)