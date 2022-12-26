import pygame
from settings import *

class Snake(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites # Usamos grupos para que al actualizar o dibujar se haga todo a la vez
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x, self.y = x, y
        # Definimos la serpiente
        self.image = pygame.Surface((TILESIZE, TILESIZE)) # 1 Cuadrado
        self.image.fill(GREEN) # Color del cuerpo
        self.rect = self.image.get_rect()
    
    def body_collision(self):
        """Controla si la cabeza de la serpiente choca con el cuerpo."""
        pass
    
    def update(self):
        # Movemos la serpiente por baldosas. Así podemos usar coordenadas más naturales
        #  y no preocuparnos de píxeles.
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Food(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        # Usamos grupos para que al actualizar o dibujar se haga todo a la vez
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x, self.y = x, y
        # Definimos la comida
        self.image = pygame.Surface((TILESIZE, TILESIZE))  # 1 Cuadrado
        self.image.fill(BLUE)  # Color de la comida
        self.rect = self.image.get_rect()
    
    def food_collision(self):
        if self.game.head.x == self.x and self.game.head.y == self.y:
            return True
        return False
    
    def update(self):        
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
