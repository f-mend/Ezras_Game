import pygame
import random

class CombatEntity:
    def __init__(self, hp, attack, defense, attack_speed, image):
        self._max_hp = hp
        self._curr_hp = self._max_hp
        self._attack = attack
        self._defense = defense
        self._attack_speed = attack_speed
        self._x = 0
        self._y = 0
        self._is_alive = True
        self._image_scale = (150,150)
        self._image = pygame.image.load(image)
        self._scaled_image = pygame.transform.scale(self._image, self._image_scale).convert_alpha()
        #rework to mask
        self._collision_rect = self._scaled_image.get_rect()
        self._collision_rect.topleft = (self._x,self._y)
        #self._collision_mask = self._scaled_image. some mask shit


    def update_unit_position(self, x, y):
        self._x = x
        self._y = y
        self._collision_rect.topleft = (self._x,self._y)
    
    def update_image_scale(self, x, y):
        self._image_scale = (x,y)

    def unit_attacks(self, target):
        target._curr_hp -= self._attack
        if target._curr_hp < 1:
            target._curr_hp = 0
            target._is_alive = False

class Player(CombatEntity):
    def __init__(self):
        super().__init__(10,6,0,3, 'Assets/player.bmp')
        self._move_speed = 5

    def unit_attacks(self, target):
       super().unit_attacks(target)
       print( f"You swing and slice them! {target._enemy_type} took {self._attack} damage")

    def unit_heals(self):
        heal_value = 10
        if (self._curr_hp + heal_value) > self._max_hp:
            heal_value = self._max_hp - self._curr_hp 
            self._curr_hp = self._max_hp
        else:
            self._curr_hp += heal_value
        
        print( f"You healed for {heal_value} hp ")


class Enemy(CombatEntity):
    def __init__(self, enemy_type, hp, attack, defense, attack_speed, image):
        super().__init__(hp, attack, defense, attack_speed, image)
        self._enemy_type = enemy_type

class Demon(Enemy):
    def __init__(self):    
        super().__init__("Demon", 12, 2, 0, 2,'Assets/Enemies/demon_enemy.bmp')

    def unit_attacks(self, target):
       super().unit_attacks(target)
       print(f"{self._enemy_type} crushed you with their wings! You took {self._attack} damage")

class Dragon(Enemy):
    def __init__(self):    
        super().__init__("Dragon", 12, 4, 0, 2,'Assets/Enemies/dragon_enemy.bmp')

    def unit_attacks(self, target):
       super().unit_attacks(target)
       print(f"{self._enemy_type} slashed you with its claws! Ewww! You took {self._attack} dong damage")

class Eye(Enemy):
    def __init__(self):    
        super().__init__("Eye", 12, 2, 0, 4,'Assets/Enemies/eye_enemy.bmp')

    def unit_attacks(self, target):
        super().unit_attacks(target)
        print(f"{self._enemy_type} stared into your soul! You took {self._attack} magic damage")

class Ghost(Enemy):
    def __init__(self):    
        super().__init__("Ghost", 12, 2, 0, 3,'Assets/Enemies/ghost_enemy.bmp')

    def unit_attacks(self, target):
        super().unit_attacks(target)
        print(f"{self._enemy_type} haunts you! You took {self._attack} spooky damage")

class SlimeKing(Enemy):
    def __init__(self):    
        super().__init__("SlimeKing", 12, 4, 0, 2,'Assets/Enemies/big_daddy.bmp')

    def unit_attacks(self, target):
       super().unit_attacks(target)
       print(f"{self._enemy_type} touched you with its slimy body! Ewww! You took {self._attack} nasty damage")


class CombatantManager():
    def __init__(self):
            #this might be creating 5 static versions of each, then i am creating copies of them to the selected enemies. This seems inefficient and could be better
            self._monsters = {
                1: Demon,
                2: Dragon,
                3: Eye,
                4: Ghost,
                5: SlimeKing
            }
            self._player = None
            self._selected_enemies = []
            self._target = []
            self._turn_counter = 0
            # -1 player lost, 0 default, 1 player won
            self._did_player_win = 0

    def value_check(self):
         print(list(self._selected_enemies))

    def generate_new_player(self):
        self._player = None
        self._player = Player()

    def generate_new_enemy(self):
        self._selected_enemies = []
        for i in range(2):
            rand = random.randint(1, 5)
            mon_class = self._monsters[rand]
            mon_instance = mon_class()  # Create a new instance of the monster
            self._selected_enemies.append(mon_instance)

    def set_target(self, target):
        self._target = target

    def did_game_end(self):
        if not self._player._is_alive:
             self._did_player_win = -1 
             return 'game_ended'
        
        i = 0
        for enemy in self._selected_enemies:
            if not enemy._is_alive:
                i+=1

        if i == len(list(self._selected_enemies)):
            self._did_player_win = 1 
            return 'game_ended'
        return None
    
    def generate_new_game(self):
        self.generate_new_player()
        self.generate_new_enemy()



