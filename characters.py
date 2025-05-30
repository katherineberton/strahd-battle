from typing import Literal, NamedTuple, Optional
import random
import time

class MoveResult(NamedTuple):
    damage: int
    strahd_stunned: bool

class PlayerClassDescription(NamedTuple):
    name: str
    attack: str
    special: str

class PlayerClass:
    name: Optional[str]
    class_name: str
    current_hp: int
    max_hp: int
    armor_class: int
    attack_mod: int
    attacks_per_attack_action: int
    damage_dice: Literal[4, 6, 8, 10, 12]
    max_specials: int
    current_specials: int
    attack_move_description: str
    special_move_description: str

    def __init__(self, name: Optional[str] = None):
        self.name = name
        self.current_hp = self.max_hp
        self.current_specials = self.max_specials

    def attack_roll(self):
        input("Roll your d20 to try to hit by pressing ENTER. ")
        to_hit = random.randint(1,20) + self.attack_mod
        print(f"Result: {to_hit}")

        return to_hit

    def attack_action(self, competing_ac: int):
        attack_damage_accumulator = 0
        attack_counter = 0

        while attack_counter < self.attacks_per_attack_action:
            if self.attack_roll() >= competing_ac:
                print("You hit!")
                damage = random.randint(1,self.damage_dice)
                attack_damage_accumulator += damage
            else:
                print("Ouch, you missed.")
            attack_counter += 1

        print(f"You did {attack_damage_accumulator} damage.")
        time.sleep(1)
        return attack_damage_accumulator
    
    def special(self, competing_ac: int):
        self.current_specials -= 1

    def take_damage(self, damage: int) -> None:
        self.current_hp -= damage

    @property
    def details(self) -> PlayerClassDescription:
        return PlayerClassDescription(
            name=self.class_name.upper(),
            attack=self.attack_move_description,
            special=self.special_move_description
        )

class Fighter(PlayerClass):
    class_name = "fighter"
    max_hp = 30
    armor_class = 20
    attack_mod = 9
    attacks_per_attack_action = 3
    damage_dice = 6
    max_specials = 3
    attack_move_description = "Swing three times with your sword (unlimited)."
    special_move_description = "Use Second Wind to gain HP (three times max)."

    def special(self, competing_ac: int):
        print("You use Second Wind!")
        input("Roll a D4 by pressing ENTER. ")
        hp_gain = random.randint(1,4) + 1

        print(f"HP gained: {hp_gain}")
        print()
        time.sleep(1)
        self.current_hp += hp_gain

        super().special(competing_ac)
        return MoveResult(damage=0, strahd_stunned=False)
    

class Caster(PlayerClass):
    class_name = "fighter"
    max_hp = 25
    armor_class = 17
    attack_mod = 8
    attacks_per_attack_action = 2
    damage_dice = 8
    max_specials = 2
    attack_move_description = "Fire two Eldritch Blasts (unlimited)."
    special_move_description = "Envelop Strahd in sunlight with Dawn (twice max)."

    def special(self, competing_ac: int):
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

        super().special(competing_ac)
        return MoveResult(damage=dawn_damage, strahd_stunned=False)

class Monk(PlayerClass):
    class_name = "monk"
    max_hp = 25
    armor_class = 20
    attack_mod = 9
    attacks_per_attack_action = 5
    damage_dice = 4
    max_specials = 3
    attack_move_description = "Punch five times in a flurry of blows (unlimited)."
    special_move_description = "Try to paralyze Strahd for a turn with a Stunning Strike (three times max)."

    def special(self, competing_ac: int):
        super().special(competing_ac)
        if self.attack_roll() >= competing_ac:
            damage = random.randint(1,10)
            print("You hit!")
            print(f"You did {damage} damage.")
            print()
            return MoveResult(damage=damage, strahd_stunned=True)
        else:
            print("Your punch bounces off his armor and Strahd shakes off the stun.")
            print()
            return MoveResult(damage=0, strahd_stunned=False)