# Shubham Patel, Teresa Yu
# File name: retro_space.py
# Date: 25 May 2022

# Links to resources used
"""
https://stackoverflow.com/questions/36510795/rotating-a-rectangle-not-image-in-pygame
https://github.com/techwithtim/Pygame-Car-Racer/blob/main/tutorial4-code/utils.py
https://stackoverflow.com/questions/30720665/countdown-timer-in-pygame
"""
# Links to images used
"""
Bullet: https://flyclipart.com/circle-yellow-circle-png-359843
Spaceship: https://creazilla.com/nodes/28428-space-fighter-clipart
Space: https://stock.adobe.com/in/search?k=cosmic%20space%20cartoon
Asteroid: https://www.nicepng.com/ourpic/u2w7e6t4w7o0i1q8_asteroid-man-boulder-clipart/
Enemy Bullet: https://www.americasfinestlabels.com/3-diam-color-code-label-fluorescent-pink-circle-p-911.html
Enemy Ship: https://www.pixilart.com/art/enemy-ship-cc5ab7a0991c5b0
"""

import pygame # Importing pygame
import math # Importing math 
import  os # Importing os for importing external file
import random # Importing the random module

pygame.mixer.init() # For adding sound effects
pygame.font.init() # For adding effects to font

# Defining constants
WIDTH, HEIGHT = 900, 500 # Setting the width and height of the window
FPS = 60 # Setting the frames per second for the window
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40 # Width and the height of the spaceship
START_POS = (WIDTH // 2 - SPACESHIP_WIDTH // 2, HEIGHT // 2 - SPACESHIP_HEIGHT // 2) # Starting position of the spaceship
MAX_VEL = 5 # Speed of the spaceship
ROTATION_VEL = 5 # Rotational velocity of the spaceship
ACCELERATION = 0.1 # Acceleration of the spaceship
BULLET_VEL = 10 # Speed of the bullet
MAX_BULLETS = 3 # Maximum bullets at a time
BULLET_TIME = 1000 # The amount of time the bullet stays on the screen
ASTEROID_VEL = 2 # Speed of the asteroids
BULLET_WIDHT, BULLET_HEIGHT = 10, 10 # Width and height of the bullets
ASTEROID_WIDHT, ASTEROID_HEIGHT = 60, 60 # Width and height of the big asteroid
ASTEROID_WIDHT_SMALL, ASTEROID_HEIGHT_SMALL = 30, 30 # Width and height of the small asteroid
WHITE = (255, 255, 255) # White color
SPACESHIP_HEALTH = 3 # Max spaceship health

# Defining some variables
clock = pygame.time.Clock() # Calling th clock function from pygame to ensure that the game runs at the correct FPS
highscore = 0 # The highscore of the user

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Setting the widht and height of the window
pygame.display.set_caption("Retro Space") # Changing the window name of the game

# Importing images
SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))     # Importing the space image and resizng it for background
SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship.png")) # Importing the spaceship image
SPACESHIP_IMAGE = pygame.transform.scale(SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)) # Changing the size of the spaceship image
BULLET_IMAGE = pygame.image.load(os.path.join("Assets", "bullet.png")) # Importing the bullet image
BULLET_IMAGE = pygame.transform.scale(BULLET_IMAGE, (BULLET_WIDHT, BULLET_HEIGHT)) # Changing the size of the spaceship image
ASTEROID_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "asteroid.png")), (ASTEROID_WIDHT, ASTEROID_HEIGHT)) # Importing the asteroid image
ASTEROID_IMAGE_SMALL = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "asteroid.png")), (ASTEROID_WIDHT_SMALL, ASTEROID_HEIGHT_SMALL)) # Importing the small asteroid image

# Importing sounds
HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "hit_sound.mp3"))
FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "fire_sound.mp3"))

# Defining custom functions for events of collision in the game
SPACESHIP_HIT = pygame.USEREVENT + 1
ASTEROID_HIT = pygame.USEREVENT + 2

# Setting the font size and style 
FONT = pygame.font.SysFont("comicsans", 40)

# Defining a class for the spaceship
class SPACESHIP:

    def __init__(self): # A function to define the various variables used for the spaceship object
        self.image = SPACESHIP_IMAGE
        self.vel = 0
        self.angle = 0
        self.x, self.y = START_POS
        self.health = spaceship_health

    def draw(self, WIN): # Defining the window() function for drawing all the elements on the window
        blit_rotate_center(WIN, self.image, (self.x, self.y), self.angle) # Calls the blit_rotate_center function

    def move_forward(self): # A function to move the spaceship forward
        self.vel = max(self.vel - ACCELERATION, MAX_VEL) # # Accelerates the spaceship
        self.move() # Calls the move function
    
    def spaceship_rotation(self, left = False, right = False): # Defines what direction the spaceship is rotating
        # Changes the angle according to the direction of rotation
        if left:
            self.angle += ROTATION_VEL
        elif right:
            self.angle -= ROTATION_VEL
    
    def move(self): # Moves the spaceship forward

        # Finding the units of movement
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        # Moving the spaceship
        self.y -= vertical
        self.x -= horizontal

        # If the spaceship goes out of the screen, brigning it back from the other side
        if self.y + SPACESHIP_HEIGHT < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0 - SPACESHIP_HEIGHT
        if self.x + SPACESHIP_WIDTH < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0 - SPACESHIP_WIDTH
    
    def reduce_speed(self):
        self.vel = max(self.vel - ACCELERATION / 2, 0) # Decelerating the spaceship to bring it to a slow halt
        self.move() # Calling the move funtion

    def shoot(self):
        bullet = BULLET() # Creating a bullet object
        bullets.append(bullet) # Adding the object to the list of bullets 

    def reset(self):
        self.x, self.y = START_POS # Reseting the position of the spaceship to the starting position
        self.angle = 0 # Reseting the angle of the spaceship
        self.vel = 0 # # Reseting the speed of the spaceship
        bullets.clear() # Clearing all the bullets from the screen


class BULLET: # Defining the bullet class

    def __init__(self): # A function to define the various variables used for the bullet object
        self.image = BULLET_IMAGE
        self.vel = BULLET_VEL
        self.angle = spaceship.angle
        self.x, self.y = spaceship.image.get_rect(topleft = (spaceship.x, spaceship.y)).center # The starting point of the bullet is the center of the spaceship
        self.start_time = pygame.time.get_ticks()
    
    def draw(self, WIN): # Defining the window() function for drawing all the elements on the window
        WIN.blit(self.image, (self.x, self.y)) # Displaying the bullets on the screen
    
    def move(self): # Moves the bulelts forward

        # Finding the units of movement
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        # Moving the bullet
        self.y -= vertical
        self.x -= horizontal

        # If the bullet goes out of the screen, brigning it back from the other side
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0

        # Removing the bullet if it has been on the screen for a certain amount of time
        if pygame.time.get_ticks() - self.start_time >= BULLET_TIME:
            bullets.remove(self)
    

class ASTEROID: # Defining the asteroid class

    def __init__(self, asteroid_image, start_pos, angle, size): # A function to define the various variables used for the spaceship object
        self.image = asteroid_image
        self.vel = ASTEROID_VEL
        self.x, self.y = start_pos
        self.angle = angle
        self.size = size
    
    def draw(self, WIN): # Defining the window() function for drawing all the elements on the window
        WIN.blit(self.image, (self.x, self.y))
    
    def move(self): # Moves the spaceship forward

        global score, highscore # Declaring the score and highscore global variables to use them inside the function

        # Finding the units of movement
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        # Moving the asteroid
        self.y -= vertical
        self.x -= horizontal

        # If the asteroid goes out of the screen, brigning it back from the other side
        if self.y + ASTEROID_HEIGHT < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0 - ASTEROID_HEIGHT
        if self.x + ASTEROID_WIDHT < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0 - ASTEROID_WIDHT
        
        asteroid_rect = self.image.get_rect(center = self.image.get_rect(topleft=(self.x, self.y)).center) # Finding the area where the asteroid is currently located
        spaceship_rect = spaceship.image.get_rect(center = spaceship.image.get_rect(topleft=(spaceship.x, spaceship.y)).center) # Finding the area where the spaceship is currently located
        
        if spaceship_rect.colliderect(asteroid_rect): # Checking if the spaceship collied with the asteroid
            spaceship.health -= 1 # Reducing the spaceship's life
            HIT_SOUND.play() # Playing the hit sound
            if spaceship.health == 0: # If the spaceship's life is 0
                if highscore < score: # Updating the highscore if the current score is a new highscore
                    highscore = score
                game_over() # Calling the game_over() function
                main() # Calling the main() function to go back to the main menu
            
            self.asteroid_split() # Calling the asteroid split function
            
            asteroids.remove(self) # Removing the current asteroid 
            spaceship.reset() # Resetting the ship
            pygame.event.post(pygame.event.Event(SPACESHIP_HIT)) # Posting a spacehsip hit event
        
        for bullet in bullets: # Checking all the bullets
            
            bullet_rect = bullet.image.get_rect(center = bullet.image.get_rect(topleft=(bullet.x, bullet.y)).center) # Finding the area where the bullet is currently located
            if bullet_rect.colliderect(asteroid_rect): # Checking if the bullet collided with the asteroid
                # Giving points to the user depending on the size of the asteroid that they shot
                if self.size == "L":
                    score += 50
                else:
                    score += 100
                bullets.remove(bullet) # Removing the bullet
                self.asteroid_split() # Calling the asteroid split function
                asteroids.remove(self) # Removing the current asteroid
                pygame.event.post(pygame.event.Event(ASTEROID_HIT)) # Posting an asteroid hit event
                
    
    def asteroid_split(self): # Spliting the asteroids into smaller asteroids
        if self.size == "L" and random.choice([True, False]): # Spliting the large asteroids into smaller ones but randomly
            
            # Giving a different angle to the two new asteroids and adding them on the screen
            small_asteroid1 = ASTEROID(ASTEROID_IMAGE_SMALL, (self.x, self.y), self.angle + 30, "S")
            small_asteroid2 = ASTEROID(ASTEROID_IMAGE_SMALL, (self.x, self.y), self.angle - 30, "S")
            asteroids.append(small_asteroid1)
            asteroids.append(small_asteroid2)


def window(WIN, spaceship): # Drawing objects on the window
    WIN.blit(SPACE, (0, 0)) # Drawing the background

    # Formatting and showing the lives text
    health_text = FONT.render("Lives: " + str(spaceship.health), 1, WHITE)
    WIN.blit(health_text, (5, 5))

    spaceship.draw(WIN) # Drawing the spaceship
    for bullet in bullets: # Drawing the bullets on the screen
        bullet.move()
        bullet.draw(WIN)
    for asteroid in asteroids: # Drawing the asteroids on the screen
        asteroid.move()
        asteroid.draw(WIN)
    pygame.display.update() # Updating the screen

def spaceship_movement(spaceship): # Defining a function to handle the spaceship's movement
    
    keys_pressed = pygame.key.get_pressed() # Cheking what keys have been pressed
    moved = False # Setting the moved variable to False

    if keys_pressed[pygame.K_UP]: # If the UP arrow key is pressed, move the spaceshp forward
        moved = True # Setting the moved variable to True
        spaceship.move_forward()
    
    if keys_pressed[pygame.K_LEFT]: # If the LEFT arrow key is pressed, rotate the spaceship left
        spaceship.spaceship_rotation(left=True)
    
    if keys_pressed[pygame.K_RIGHT]: # If the RIGHT arrow key is pressed, rotate the spaceship right
        spaceship.spaceship_rotation(right=True)

    if not moved: # If the spaceship has not moved, reduce the speed
        spaceship.reduce_speed()

def blit_rotate_center(WIN, image, top_left, angle): # Function to rotate the spaceship
    rotated_image = pygame.transform.rotate(image, angle) # Rotating the image with the specified angle
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft=top_left).center) # Setting the rotated image at the same center as the original image
    WIN.blit(rotated_image, new_rect.topleft) # Drawing the new image

def get_start_pos(): # Generating a random starting point for the asteroids

    axis = [0, 1]

    if (random.choice(axis) == 0):
        x = random.randint(0, WIDTH)
        y = 0
    else:
        x = 0
        y = random.randint(0, HEIGHT)
        
    return x, y
    
def get_angle(): # Generating a random angle for the asteroids
    return random.randint(0, 360)

def level_text(level): # Showing the level text for two seconds before moving on with the game
    level_text = FONT.render("Level: " + str((level - 1) // 2), 1, WHITE)
    WIN.blit(SPACE, (0, 0))
    WIN.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - level_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)

def main_menu_text(): # Showing the main menu text, including title, start, instruction, highscore, etc.
    title_text = FONT.render("R E T R O   S P A C E   B L A S T E R", 1, WHITE)
    start_text = FONT.render("START (press enter)", 1, WHITE)
    instruction_text = FONT.render("INSTRUCTIONS (press I)", 1, WHITE)
    highscore_text = FONT.render("Highscore: " + str(highscore), 1, WHITE)
    WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
    WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 150))
    WIN.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, 250))
    WIN.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, 350))

def instructions(): # Showing the instructions text
    title_text = FONT.render("I N S T R U C T I O N S", 1, WHITE)
    text1 = FONT.render("Use arrow keys to rotate and move forward.", 1, WHITE)
    text2 = FONT.render("Hit the space key to shoot the asteroids.", 1, WHITE)
    text3 = FONT.render("To win a level, remove all the asteroids.", 1, WHITE)
    text4 = FONT.render("Press Esc to exit", 1, WHITE)
    run = True # Creating a variable for running the while loop
    while run: # Running the main while loop
        clock.tick(FPS) # Calling the tick functin to set FPS for the while loop

        for event in pygame.event.get(): # Checking for events in the game
            
            if event.type== pygame.QUIT: # Checking if the event is quiting the game
                run = False # Changing the iteration variable to False
                pygame.quit() # Exiting pygame
            
            if event.type == pygame.KEYDOWN: # Checking if the event is pressing a key
                if event.key == pygame.K_ESCAPE: # Checking if the pressed key is escape
                    main() # Going back to the main menu
        
        # Displaying the text on the screen
        WIN.blit(SPACE, (0, 0))
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 30))
        WIN.blit(text1, (WIDTH // 2 - text1.get_width() // 2, 100))
        WIN.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 180))
        WIN.blit(text3, (WIDTH // 2 - text3.get_width() // 2, 260))
        WIN.blit(text4, (WIDTH // 2 - text4.get_width() // 2, 350))
        pygame.display.update()

def game_over(): # Showing the GAME OVER text for two seconds
    text = FONT.render("G A M E   O V E R", 1, WHITE)
    text1 = FONT.render("Score: " + str(score), 1, WHITE)
    text2 = FONT.render("NEW HIGHSCORE!", 1, WHITE)
    WIN.blit(SPACE, (0, 0))
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))
    WIN.blit(text1, (WIDTH // 2 - text1.get_width() // 2, 200))
    if score == highscore: # Displaying the NEW HIGHSCORE text if the player made a new highscore
        WIN.blit(text2, (WIDTH // 2 - text2.get_width() // 2, 300))
    pygame.display.update()
    pygame.time.delay(2000)

def levels(level):

    # Defining some global variables
    global bullets, asteroids
    bullets = []
    asteroids = []

    for x in range(level): # Creating asteroid objects and adding them to the asteroids list
        asteroids.append(ASTEROID(ASTEROID_IMAGE, get_start_pos(), get_angle(), "L"))

    level_text(level) # Calling the level text function

    run = True # Creating a variable for running the while loop
    while run: # Running the main while loop
        clock.tick(FPS) # Calling the tick functin to set FPS for the while loop

        for event in pygame.event.get(): # Checking for events in the game
            
            if event.type== pygame.QUIT: # Checking if the event is quiting the game
                run = False # Changing the iteration variable to False
                pygame.quit() # Exiting pygame
        
            if event.type == pygame.KEYDOWN: # Checking if the event is pressing a key
                if event.key == pygame.K_SPACE: # Checking if the pressed key is space 
                    if len(bullets) < MAX_BULLETS: # If the bullets on the screen is less than the max bullets allowed, playing the fire sound and shooting a bullet
                        FIRE_SOUND.play()
                        spaceship.shoot()

            if event.type == SPACESHIP_HIT: # Checking if the spaceship is hit
                if len(asteroids) == 0: # If all the asteroids on the screen are removed, going to the next level
                    level += 2
                    levels(level)
            
            if event.type == ASTEROID_HIT: # Checking if the asteroid is hit
                HIT_SOUND.play() # Playing the hit sound
                if len(asteroids) == 0: # If all the asteroids on the screen are removed, going to the next level
                    level += 2
                    levels(level)

        spaceship_movement(spaceship) # Calling the spacehip_movement() function to check for spaceship's movement

        window(WIN, spaceship) # Calling the window 


def main(): # The main menu functions

    # Defining some global variables 
    global spaceship, score, spaceship_health
    spaceship_health = SPACESHIP_HEALTH
    score = 0
    spaceship = SPACESHIP() # Creating the spaceship object
    level = 3 # The number of asteroids that the game starts with is 3

    run = True # Creating a variable for running the while loop
    while run: # Running the main while loop
        clock.tick(FPS) # Calling the tick functin to set FPS for the while loop

        for event in pygame.event.get(): # Checking for events in the game
            
            if event.type== pygame.QUIT: # Checking if the event is quiting the game
                run = False # Changing the iteration variable to False
                pygame.quit() # Exiting pygame
        
            if event.type == pygame.KEYDOWN: # Checking if any keys are pressed
                if event.key == pygame.K_RETURN: # Checking if the enter key is pressed
                    levels(level) # Calling the levels function
            
            if event.type == pygame.KEYDOWN: # Checking if any keys are pressed
                if event.key == pygame.K_i: # Checking if 'i' key is pressed
                    instructions() # Goes to the instructions page
        
        WIN.blit(SPACE, (0, 0)) # Drawing the background
        main_menu_text() # Calling the function to print text on the main menu
        pygame.display.update() # Updating the display

if (__name__  == "__main__"): # Making sure that the game only starts if the file is opened directly
  main()