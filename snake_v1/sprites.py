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
        if self.x == self.game.head.x and self.y == self.game.head.y:
            return True
        return False
    
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

class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.text = text
    
    def draw(self, screen, font_size):
        font = pygame.font.SysFont("Arial", font_size)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))

class Button:
    def __init__(self, game, color, outline, x, y, width, height, text):
        self.game = game
        self.color, self.outline = color, outline
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.text = text
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(self.text, True, WHITE)
        draw_x = self.x + (self.width / 2 - text.get_width() / 2)
        draw_y = self.y + (self.height / 2 - text.get_height() / 2)
        screen.blit(text, (draw_x, draw_y))
    
    def is_over(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

