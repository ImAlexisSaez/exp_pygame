import pygame

from settings import *

# Inicializamos la fuente:
pygame.font.init()

# Clase "Baldosa"
class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        # Asignamos los grupos de Sprites (para dibujarlos todos de golpe)
        self.groups = game.all_sprites

        # Inicializamos la clase Sprite de donde heredamos
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.x, self.y = x, y
        self.text = text

        # Creamos imagen con el tamaño de cada baldosa
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()

        # Comprobamos si el texto es 'empty' para dibujar acorde:
        if self.text != 'empty':
            self.font = pygame.font.SysFont("Consolas", 50)
            font_surface = self.font.render(self.text, True, BLACK)
            self.image.fill(WHITE)  # Cuadrado blanco
            self.font_size = self.font.size(self.text) # Devuelve una tupla con las dimensiones del texto
            #self.image.blit(font_surface, (self.x, self.y)) # Números no centrados
            draw_x = TILESIZE / 2 - self.font_size[0] / 2
            draw_y = TILESIZE / 2 - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill(BGCOLOR) # La baldosa vacía es del color del fondo.
    
    def update(self):
        # Pasamos los índices y al multiplicar por TILESIZE tendremos
        #  exactamente las coordenadas para actualizar.
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
    
    def click(self, mouse_x, mouse_y):
        # Comprueba si hacemos click en una baldosa
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom
    
    # Funciones que evalúan si al hacer clic en una baldosa, las que se ubican
    #  a izquierda, derecha, arriba y abajo están dentro de la rejilla.
    def right(self):
        return self.rect.x + TILESIZE < GAME_SIZE * TILESIZE

    def left(self):
        return self.rect.x - TILESIZE >= 0

    def up(self):
        return self.rect.y - TILESIZE >= 0

    def down(self):
        return self.rect.y + TILESIZE < GAME_SIZE * TILESIZE

class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text
    
    def draw(self, screen):
        font = pygame.font.SysFont("Consolas", 50)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))


class Button:
    def __init__(self, x, y, width, height, text, colour, text_colour):
        self.colour, self.text_colour = colour, text_colour
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Consolas", 30)
        text = font.render(self.text, True, self.text_colour)
        self.font_size = font.size(self.text)
        draw_x = self.x + self.width / 2 - self.font_size[0] / 2
        draw_y = self.y + self.height / 2 - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))

    def click(self, mouse_x, mouse_y):
        # Comprueba si hacemos click en una baldosa
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height
