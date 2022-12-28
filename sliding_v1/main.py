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
        # Variables para el barajado de baldosas
        self.shuffle_time = 0
        self.start_shuffle = False
        self.previous_choice = ''
        # Variable para controlar el estado del juego
        #  Cuando bajaremos pasará a True
        self.start_game = False
        self.start_timer = 0
        self.elapsed_time = 0
    
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
    
    def shuffle(self):
        # Busca la baldosa vacía, mira las que tiene al lado dentro de la rejilla,
        #  escoge una al azar y la intercambia (como si jugara al azar el pc).
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == 'empty':
                    if tile.right():
                        possible_moves.append("right")
                    # No hacer elif, pues hay varias posibilidades y hay que comprobarlas todas
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            # Si hay movimientos posibles, dejamos de recorrer bucles
            if len(possible_moves) > 0:
                break
        
        # Además, queremos controlar que si fue hacia la derecha, en el siquiente movimiento
        #  no vaya hacia la izquierda (estaría volviendo entonces la rejilla a la misma
        #  posición en la que estaba).
        if self.previous_choice == 'right':
            possible_moves.remove('left') if 'left' in possible_moves else possible_moves
        elif self.previous_choice == 'left':
            possible_moves.remove('right') if 'right' in possible_moves else possible_moves
        elif self.previous_choice == 'up':
            possible_moves.remove('down') if 'down' in possible_moves else possible_moves
        elif self.previous_choice == 'down':
            possible_moves.remove('up') if 'up' in possible_moves else possible_moves
        
        
        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == 'right':
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
        elif choice == 'left':
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]
        elif choice == 'up':
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
        elif choice == 'down':
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]



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
    
        # Dibujamos las baldosas:
        self.draw_tiles()

        # Textos del juego:
        

        # Botones del juego
        self.buttons_list = []
        self.buttons_list.append(Button(775, 100, 200, 50, "Shuffle", WHITE, BLACK))
        self.buttons_list.append(Button(775, 170, 200, 50, "Reset", WHITE, BLACK))

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
        
        # Barajamos
        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 120: # Como los FPS son 60, son 2 segundos.
                self.start_shuffle = False


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

        # Dibujamos los textos del juego:
        

        # Dibujamos los botones del juego:
        for button in self.buttons_list:
            button.draw(self.screen)
        
        # Un vez hemos terminado de dibujar, debemos llamar esta función:
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            # Cerramos el juego con la X.
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            
            # Si hacemos clic:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Tomamos la posición del clic:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            # Comprobamos si hay una baldosa en la rejilla a la derecha
                            #  y si esa baldosa es 0 (la vacía), las intercambiamos.
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]
                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]
                            # Acabadas las comprobaciones, dibujamos la rejilla de nuevi
                            self.draw_tiles()

                # Comprobamos si pulsamos los botones
                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            # Resetamos el temporizador al barajar
                            # Moveremos baldosas por 5 segundos
                            self.shuffle_time = 0
                            self.start_shuffle = True
                        if button.text == "Reset":
                            self.new()




# Creamos una instancia del juego
game = Game()
while True:
    game.new() # Creamos un nuevo juego
    game.run() # Empezamos el nuevo juego
        