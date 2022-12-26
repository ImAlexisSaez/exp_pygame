import pygame
import random
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
        self.paused = False
        self.playing = True
        self.score = 0
        self.high_score = self.get_high_score()
    
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

        
    
    def is_body_part(self):
        """Comprobamos que la nueva comida no sea una parte de la serpiente."""
        # check the coords agains the body of the snake
        x = random.randint(0, GRIDWIDTH - 1) # -1 para no poner fuera la comida del borde
        y = random.randint(0, GRIDHEIGHT - 1)
        for body in self.snake_parts:
            if x == body.x and y == body.y:
                self.is_body_part()
        return x, y



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
        if not self.paused:
            # Check if the snake eats the food
            if self.food.food_collision():
                # "Borramos" la comida, moviéndola de posición.
                x, y = self.is_body_part()
                self.food.x = x
                self.food.y = y
                # Añadimos una parte a la serpiente.
                self.snake_parts.append(Snake(self, self.snake_parts[-1].x, self.snake_parts[-1].y))
                # Ganamos un punto
                self.score += 1
                

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
            
            # check for body collision
            # - Comprobamos si alguna de las coordenadas del cuerpo es igual
            #   a las coordenadas de la cabeza de la serpiente.
            for body in self.snake_parts:
                if body.body_collision():
                    self.playing = False
            
            # send snake to other side of the screen
            if self.head.x > GRIDWIDTH - 1:
                self.head.x = 0
            elif self.head.x < 0:
                self.head.x = GRIDWIDTH
            elif self.head.y > GRIDHEIGHT - 1:
                self.head.y = 0
            elif self.head.y < 0:
                self.head.y = GRIDHEIGHT

        

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
        if self.paused:
            UIElement(10, 10, "PAUSED").draw(self.screen, 100)     
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
                if not self.paused:
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
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
    
    def get_high_score(self):
        # Cuidado con la ruta al archivo, pues el directorio de trabajo no es
        #  el de snake_v1, sino el superior, el de exp_pygame.
        with open("snake_v1/high_score.txt", "r") as file:
            score = file.read()
        return int(score)

    def save_score(self):
        with open("snake_v1/high_score.txt", "w") as file:
            if self.score > self.high_score:
                file.write(str(self.score))
            else:
                file.write(str(self.high_score))
    
    def main_screen(self):
        self.save_score()
        self.screen.fill(BGCOLOR)
        if not self.playing:
            UIElement(8, 7, "GAME OVER").draw(self.screen, 100)
            UIElement(14, 13, f"Score: {self.score}").draw(self.screen, 30)
        else:
            UIElement(8, 7, "SNAKE GAME").draw(self.screen, 100)
        
        UIElement(13, 11, f"High score: {self.high_score if self.high_score > self.score else self.score}").draw(self.screen, 30)

        # buttons
        self.start_button = Button(self, BGCOLOR, WHITE, WIDTH / 2 - 150 / 2, 470, 150, 50, "START")
        self.quit_button = Button(self, BGCOLOR, WHITE, WIDTH / 2 - 150 / 2, 545, 150, 50, "QUIT")
        self.wait()
    
    def wait(self):
        waiting = True
        while waiting:
            self.start_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                # Si pulsamos la X
                if event.type == pygame.QUIT:
                    self.quit()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEMOTION:
                    if self.start_button.is_over(mouse_x, mouse_y):
                        self.start_button.color = LIGHTGREY
                    else:
                        self.start_button.color = BGCOLOR
                    if self.quit_button.is_over(mouse_x, mouse_y):
                        self.quit_button.color = LIGHTGREY
                    else:
                        self.quit_button.color = BGCOLOR
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.is_over(mouse_x, mouse_y):
                        waiting = False
                    if self.quit_button.is_over(mouse_x, mouse_y):
                        self.quit()



# Creación del juego
game = Game()

# Bucle infinito
while True:
    # Pantalla de inicio del juego
    game.main_screen()
    game.new()
    game.run()
