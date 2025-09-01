from typing import Literal, NamedTuple, Optional
import random
import time

class MoveResult(NamedTuple):
    damage: int
    stunned: bool

class PlayerClassDescription(NamedTuple):
    name: str
    attack: str
    special: str

class PlayerClass:
    name: Optional[str]
    class_name: str
    armor_class: int

    max_hp: int
    current_hp: int

    attack_mod: int
    attacks_per_attack_action: int
    damage_dice: Literal[4, 6, 8, 10, 12]
    number_of_damage_dice: int = 1
    damage_modifier: int = 0
    attack_move_description: str

    current_specials: int
    max_specials: int
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

                single_atk_dmg_accumulator = 0
                for _ in range(self.number_of_damage_dice):
                    single_atk_dmg_accumulator += random.randint(1,self.damage_dice)
                single_atk_dmg_accumulator += self.damage_modifier

                attack_damage_accumulator += single_atk_dmg_accumulator
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
        return MoveResult(damage=0, stunned=False)
    

class Caster(PlayerClass):
    class_name = "caster"
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
        return MoveResult(damage=dawn_damage, stunned=False)

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
            return MoveResult(damage=damage, stunned=True)
        else:
            print("Your punch bounces off his armor and Strahd shakes off the stun.")
            print()
            return MoveResult(damage=0, stunned=False)
        

class Strahd(PlayerClass):
    class_name = "strahd"
    max_hp = 40
    armor_class = 16
    attack_mod = 12
    attacks_per_attack_action = 2
    damage_dice = 4
    number_of_damage_dice = 1
    damage_modifier = 2
    max_specials = 2
    last_move: Optional[Literal["bite", "claw"]] = None
    stunned: bool = False

    def attack(self, competing_ac: int):
        """randomizes Strahd's claw attack or bite attack"""

        if random.choice(['bite', 'claw']) == 'claw':
            dmg = self.attack_action(competing_ac)
        else:
            dmg = self.special(competing_ac)
        
        print()
        time.sleep(1)
        return dmg

    # Overriding the attack_action method for additional exposition
    def attack_action(self, competing_ac: int) -> int:
        print("Strahd extends his claws and rears back with both hands.")

        claw_damage_accumulator = 0
        attack_counter = 0

        while attack_counter < self.attacks_per_attack_action:
            attack_to_hit = random.randint(1,20) + self.attack_mod
            if attack_to_hit >= competing_ac:
                print("Strahd slashes at you with a claw.")
                damage = random.randint(1,4) + 2
                claw_damage_accumulator += damage
            else:
                print("You are just out of his reach!")
            attack_counter += 1
        
        print(f"Strahd did {claw_damage_accumulator} damage.")
        self.last_move = "claw"
        return claw_damage_accumulator
    
    def special(self, competing_ac: int) -> MoveResult:
        bite_damage = 0
        if random.randint(1,20) + self.attack_mod >= competing_ac:
            print("Strahd sinks his fangs into you!")
            bite_damage += random.randint(1,6)
            bite_damage += random.randint(1,6)
            print(f"Strahd did {bite_damage} damage.")

        else:
            print("Strahd lunges for your exposed neck but misses!")
        self.last_move = "bite"
        return bite_damage