# The Libraries:
import pygame                     # For game development
from pygame.locals import *       # To use constants like QUIT, etc.
import random                     # For random number generation

# Initialization:
pygame.init()                     # Initializes all pygame modules

# Display Values:
screen_width = 550                # Width of the game window
screen_height = 650               # Height of the game window

# The Game Window:
screen = pygame.display.set_mode((screen_width, screen_height))   # Creates the game screen

# The Caption On The Top Left:
pygame.display.set_caption("Flappy Bird")     # Sets the window title

# These Are All The Required Variables:

clock = pygame.time.Clock()                   # Controls the game's frame rate
fps = 60                                       # Maximum number of frames per second

ground_scroll = 0                              # Horizontal scroll offset for the ground
scroll_speed = 3                               # How fast the ground and pipes move
flying = False                                 # Flag to check if the bird has started flying
game_over = False                              # Flag to check if the game is over
pipe_gap = 150                                 # Vertical space between top and bottom pipes
pipe_freq = 1500                               # Frequency of pipe generation in milliseconds
last_pipe = pygame.time.get_ticks() - pipe_freq  # Time when the last pipe was generated
score = 0                                      # Player's score
pass_pipe = False                              # Flag to check if bird has passed a pipe

font = pygame.font.SysFont('Bauhaus 93', 60)   # Font used for displaying the score
White = (255, 255, 255)                        # Color used for score text

# Function To Draw Text On Screen:
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)    # Renders the text into an image
    screen.blit(img, (x, y))                   # Draws the image on the screen

# Function To Reset Game State:
def reset():
    pipe_group.empty()                         # Clears all pipes from the screen
    flappy.rect.x = 80                         # Resets bird's x position
    flappy.rect.y = int(screen_height / 2)     # Resets bird's y position
    score = 0                                  # Resets the score
    return score

# The Bird Class:
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)    # Initializes the Sprite parent class
        self.images = []                       # List to hold bird animation images
        self.index = 0                         # Current frame index
        self.counter = 0                       # Frame counter
        for num in range(1, 4):
            img = pygame.image.load(fr"C:\\Users\\User\\OneDrive\\PythonCodes.py\\flappy_square_project\\bird{num}.png").convert_alpha()  # Loads bird image
            self.images.append(img)            # Adds image to list
        self.image = self.images[self.index]   # Sets initial image
        self.rect = self.image.get_rect()      # Gets image rectangle
        self.rect.center = [x, y]              # Sets initial position
        self.velocity = 0                      # Initial velocity
        self.clicked = False                   # Tracks mouse click status

    def update(self):
        if flying:
            self.velocity += 0.4               # Simulates gravity
            if self.velocity > 5:
                self.velocity = 5              # Caps downward speed
            if self.rect.bottom < 500:
                self.rect.y += int(self.velocity)   # Applies gravity to bird
            if self.rect.top <= 0:
                self.rect.top = 0              # Prevents bird from going off top
                if self.velocity < 0:
                    self.velocity = 0          # Stops upward velocity off-screen

        if not game_over:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True            # Detects fresh mouse click
                self.velocity -= 10            # Makes bird jump
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False           # Resets click flag when mouse released

            self.counter += 1                  # Updates animation frame counter
            cooldown = 10                     # Time between frames
            if self.counter >= cooldown:
                self.counter = 0
                self.index += 1                # Switches to next animation frame
                if self.index >= len(self.images):
                    self.index = 0             # Loops animation
            self.image = pygame.transform.rotate(self.images[self.index], -self.velocity * 2)  # Rotates bird based on velocity
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)  # Tilt bird when dead

# The Pipe Class:
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)    # Initializes Sprite
        self.image = pygame.image.load(r'C:\\Users\\User\\OneDrive\\PythonCodes.py\\flappy_square_project\\pipe.png')  # Loads pipe image
        self.rect = self.image.get_rect()      # Gets rectangle of image

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)  # Flips pipe for top
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]  # Positions top pipe
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]     # Positions bottom pipe

    def update(self):
        self.rect.x -= scroll_speed            # Moves pipe to the left
        if self.rect.right < 0:
            self.kill()                        # Deletes pipe if off screen

# Initializes the bird:
flappy = Bird(80, int(screen_height / 2))      # Places bird in the center

# The Button Class:
class Button():
    def __init__(self, x, y, image):
        self.image = image                     # Sets button image
        self.rect = self.image.get_rect()      # Gets image rectangle
        self.rect.center = (x, y)              # Sets position

    def draw(self):
        action = False                         # Tracks if button was clicked
        pos = pygame.mouse.get_pos()           # Gets mouse position
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True                  # Button was clicked
        screen.blit(self.image, (self.rect.x, self.rect.y))   # Draws button
        return action

# Sprite Groups:
bird_group = pygame.sprite.Group()            # Group to hold bird
bird_group.add(flappy)                        # Adds bird to group
pipe_group = pygame.sprite.Group()            # Group to hold pipes

# Load Images:
restart_button = pygame.image.load(r"C:\\Users\\User\\OneDrive\\PythonCodes.py\\flappy_square_project\\restart.png")  # Restart button image
button = Button(screen_width // 2, screen_height // 2, restart_button)   # Places button

bg = pygame.image.load(r'flappy_square_project\\background.png')       # Background image
ground_img = pygame.image.load(r"C:\\Users\\User\\OneDrive\\PythonCodes.py\\flappy_square_project\\ground.png")  # Ground image

# The Game Loop:
run = True
while run:
    clock.tick(fps)                            # Limits the loop to 60 FPS

    screen.blit(bg, (0, 0))                    # Draws background image
    pipe_group.draw(screen)                    # Draws all pipes
    screen.blit(ground_img, (ground_scroll, 500))  # Draws ground image

    if len(pipe_group) > 0:
        pipe = pipe_group.sprites()[0]         # Gets first pipe
        bird = bird_group.sprites()[0]         # Gets the bird

        if bird.rect.left > pipe.rect.left and bird.rect.right < pipe.rect.right and not pass_pipe:
            pass_pipe = True                   # Bird is between pipe edges
        if pass_pipe and bird.rect.left > pipe.rect.right:
            score += 1                         # Bird passed pipe — score +1
            pass_pipe = False

    draw_text(str(score), font, White, int(screen_width / 2), 20)   # Draws score text

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        game_over = True                       # Bird hits pipe

    if flappy.rect.bottom > 500:
        game_over = True                       # Bird hits ground
        flying = False                         # Bird stops flying

    if not game_over and flying:
        time_now = pygame.time.get_ticks()     # Gets current time
        if time_now - last_pipe > pipe_freq:
            pipe_height = random.randint(-150, 150)   # Random pipe height
            btm_pipe = Pipe(screen_width, screen_height / 2 + pipe_height, -1)  # Bottom pipe
            top_pipe = Pipe(screen_width, screen_height / 2 + pipe_height, 1)   # Top pipe
            pipe_group.add(btm_pipe)          # Adds bottom pipe
            pipe_group.add(top_pipe)          # Adds top pipe
            last_pipe = time_now              # Updates last pipe time

        ground_scroll -= scroll_speed          # Moves ground
        if abs(ground_scroll) > 25:
            ground_scroll = 0                 # Resets scroll
        pipe_group.update()                   # Updates pipe positions

    bird_group.draw(screen)                   # Draws bird
    bird_group.update()                       # Updates bird position

    if game_over:
        if button.draw():
            game_over = False
            score = reset()                   # Resets game if restart clicked

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False                        # Ends game loop
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True                      # Starts game on click

    pygame.display.update()                    # Updates display

pygame.quit()                                  # Quits pygame
