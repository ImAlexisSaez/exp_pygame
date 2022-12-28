import pygame
import random
import time

from sprites import *
from settings import *

class Game:
    def __init__(self):
        # Inicializamos el módulo pygame
        pygame.init() 
        # Declaramos la pantalla:
        # - Las dimensiones van en una tupla
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # Título del juego:
        pygame.display.set_caption(TITLE)
        # Reloj:
        self.clock = pygame.time.Clock()
    
    def create_game(self):
        # Crea el juego propiamente dicho y es la condición de ganar partida también.
        #[
        #    [1, 2, 3],
        #    [4, 5, 6],
        #    [7, 8, 0] # 0 para la baldosa "vacía"
        #]
        grid = []
        number = 1 # Los números del juego

        for x in range(GAME_SIZE):
            grid.append([])
            for y in range(GAME_SIZE):
                grid[x].append(number)
                number += 1
        
        # Bucle con list comprehension
        #grid = [[x+ y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]

        grid[-1][-1] = 0  # Cambiamos el último número por un 0.

        return grid

    def draw_tiles(self):
        self.tiles = []

        # Cogemos, de la rejilla, el índice del elemento y el número que contiene:
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0: # Entonces dibujamos, porque no es la "vacía".
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    # Con el texto 'empty' luego controlaremos ese espacio vacío.
                    self.tiles[row].append(Tile(self, col, row, "empty"))


    def new(self):
        # Asignamos los grupos de Sprites
        self.all_sprites = pygame.sprite.Group()

        # Crea la rejilla, que irá cambiando cada vez que pulsemos en una baldosa.
        self.tiles_grid = self.create_game()

        # Para comprobar si se gana la partida
        self.tiles_grid_completed = self.create_game()

    def run(self):
        self.playing = True # Bandera para controlar si acaba el juego.
        while self.playing:
            # Iniciamos el reloj
            self.clock.tick(FPS)
            # Controlamos eventos
            self.events()
            # Actualizamos según eventos
            self.update()
            # Dibujamos si procede
            self.draw()

    def update(self):
        # Actualizamos los sprites
        self.all_sprites.update()

    def draw_grid(self):
        # Dibujamos la rejilla
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, GAME_SIZE * TILESIZE))
        
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (GAME_SIZE * TILESIZE, col))

    def draw(self):
        # Rellenamos la pantalla con el color de fondo:
        self.screen.fill(BGCOLOR) 

        # Dibujamos los sprites:
        self.all_sprites.draw(self.screen)      

        # Dibujamos la rejilla que contiene los números
        self.draw_grid()

        # Dibujamos las baldosas:
        self.draw_tiles()

        # Un vez hemos terminado de dibujar, debemos llamar esta función:
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            # Cerramos el juego con la X.
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)


# Creamos una instancia del juego
game = Game()
while True:
    game.new() # Creamos un nuevo juego
    game.run() # Empezamos el nuevo juego
        