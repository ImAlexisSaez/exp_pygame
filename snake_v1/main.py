import pygame
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        # Orientación de la serpiente
        self.orientation = 0
    
    def new(self):
        """Juego nuevo."""
        self.all_sprites = pygame.sprite.Group()
        # Dibujamos la cabeza de la serpiente.
        self.head = Snake(self, 10, 10)
        # Cuerpo de la serpiente
        # - Cada vez que comamos, añadimos otra "cabeza" de serpiente.
        # - Cada elemento de la lista "seguirá" al anterior. El primero a la cabeza,
        #   el segundo al primero, etc.
        self.snake_parts = []
        self.snake_parts.append(Snake(self, 9, 10))
        self.snake_parts.append(Snake(self, 8, 10))

        # Comida
        self.food = Food(self, 20, 10)


    def run(self): 
        # game loop - set self.playing to False to end the game
        self.playing = True
        while self.playing:
            self.clock.tick(SPEED) # Los FPS vienen dados por la velocidad de la serpiente
            self.events() # Miramos si hay algún evento (clics...)
            self.update() # Actualizamos en consecuencia
            self.draw() # Dibujamos

    def quit(self):
        """Cierra el juego al hacer clic sobre la X."""
        pygame.quit()
        quit(0) # No muestra errores al cerrar.
    
    def update(self):        

        # Check if the snake eats the food
        if self.food.food_collision():
            # Añadimos una parte a la serpiente.
            self.snake_parts.append(Snake(self, self.snake_parts[-1].x, self.snake_parts[-1].y))
            # "Borramos" la comida, moviéndola de posición.

        # Update all sprites
        self.all_sprites.update()

        # Movimiento de las partes de la serpiente.
        x, y = self.head.x, self.head.y
        for body in self.snake_parts:
            temp_x, temp_y = body.x, body.y
            body.x, body.y = x, y
            x, y = temp_x, temp_y

        # Movemos la serpiente.        
        # Orientemos la serpiente según las teclas.
        # 0 derecha, 1 arriba, 2 izquierda, 3 abajo
        if self.orientation == 0:
            self.head.x += 1
        elif self.orientation == 1:
            self.head.y -= 1
        elif self.orientation == 2:
            self.head.x -= 1
        elif self.orientation == 3:
            self.head.y += 1

    def draw_grid(self):
        """Dibuja la rejilla de baldosas."""
        for row in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row, 0), (row, HEIGHT))
        for col in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, col), (WIDTH, col))

    def draw(self):
        self.screen.fill(BGCOLOR) # Limpia la pantalla con el color de fondo
        self.all_sprites.draw(self.screen)
        self.draw_grid()        
        pygame.display.flip() # Para dibujar algo necesitamos flip() la pantalla

    def events(self):
        # catch all events
        for event in pygame.event.get():
            # Si pulsamos la X
            if event.type == pygame.QUIT:
                self.quit()
            # Controlamos la orientación de la serpiente
            # - Comprobamos también si la orientación no es la opuesta a la que
            #   hay, pues moriríamos por ir en el sentido contrario.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if not self.orientation == 3:
                        self.orientation = 1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if not self.orientation == 1:
                        self.orientation = 3
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if not self.orientation == 0:
                        self.orientation = 2
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if not self.orientation == 2:
                        self.orientation = 0
                



# Creación del juego
game = Game()

# Bucle infinito
while True:
    game.new()
    game.run()
