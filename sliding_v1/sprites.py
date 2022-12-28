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
