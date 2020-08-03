import pygame
import random
import time
import os
pygame.font.init()

# Defining the window
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arrow Defense")

# Load images
PLAYER_IMG = pygame.image.load(os.path.join("assets", "whitePlayer.png"))
ARROW_IMG = pygame.image.load(os.path.join("assets", "arrow_img.png"))
ENEMY_IMG = pygame.image.load(os.path.join("assets", "enemy_img.png"))
# Background image
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

class Character():
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.character_img = None
        self.arrow_img = None
        self.arrows = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.character_img, (self.x, self.y))

    def get_width(self):
        return self.character_img.get_width()

    def get_height(self):
        return self.character_img.get_height()

    def flip(self):
        self.character_img = pygame.transform.flip(self.character_img, True, False)

    def get_direction(self):
        return self.direction

    def set_direction(self, direction):
        self.direction = direction

class Arrow():
    def __intit__(self, x, y):
        self.x = x
        self.y = y
        self.arrow_img = ARROW_IMG
        self.mask = pygame.mask.from_surface(self.arrow_img)
    def draw(self, window):
        window.blit(self.arrow_img, (self.x, self.y))
    def move(self, xvel, yvel):
        self.x += xvel
        self.y += yvel

class Enemy(Character):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.character_img = ENEMY_IMG
        self.mask = pygame.mask.from_surface(self.character_img)
        self.direction = ""
    def move(self, xvel, yvel):
        self.x += xvel
        self.y += yvel


class Player(Character):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.character_img = PLAYER_IMG
        self.arrow_img = ARROW_IMG
        self.mask = pygame.mask.from_surface(self.character_img)
        self.max_health = health
        self.direction = "RIGHT" 
    

def main():
    run = True
    FPS = 60
    lives = 5
    level = 0
    score = 0
    player_vel = 5
    clock = pygame.time.Clock()
    enemies = []
    wave_length = 5
    enemy_vel = 1

    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    player = Player(WIDTH/2 - PLAYER_IMG.get_width()/2, 300)

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        for enemy in enemies[:]:
            enemy.draw(WIN)

        player.draw(WIN)

        WIN.blit(lives_label, (10, 10))
        WIN.blit(score_label, (WIDTH - score_label.get_width() - 10, 10))
        WIN.blit(level_label, (WIDTH/2 - level_label.get_width()/2, 10))

        if lost:
            lost_label = lost_font.render(f"You lost! Score: {score}", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 300))
        
        pygame.display.update()

    
    while run:
        clock.tick(FPS) # Runs at a specific rate regardless of hardware
        redraw_window()
        
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        if lost:
            if lost_count > FPS * 5:
                run = False
            else:
                continue # Go back to the beginning of the loop

        # Spawning the enemies in
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                xL = random.randrange(-1500, -50)
                xR = random.randrange(WIDTH+50, WIDTH+1500)
                yU = random.randrange(-1500, -50)
                yD = random.randrange( HEIGHT+50, HEIGHT+1500)
                xRange = [xL, xR]
                yRange = [yU, yD]
                enemy = Enemy(random.choice(xRange), random.choice(yRange))
                enemies.append(enemy)

        # Exits the window when you press the X button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
            if player.get_direction() == "RIGHT":
                player.flip()
            player.set_direction("LEFT")
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
            if player.get_direction() == "LEFT":
                player.flip()
                
            player.set_direction("RIGHT")
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: # down
            player.y += player_vel
        
        # Moving the enemies towards the player
        for enemy in enemies[:]:
            if enemy.x >= player.x and enemy.y >= player.y:
                enemy.move(-enemy_vel, -enemy_vel) # Move up and left
                if enemy.get_direction() == "RIGHT":
                    enemy.flip()
                enemy.set_direction("LEFT")
            if enemy.x >= player.x and enemy.y <= player.y:
                enemy.move(-enemy_vel, enemy_vel) # Move down and left
                if enemy.get_direction() == "RIGHT":
                    enemy.flip()
                enemy.set_direction("LEFT")
            if enemy.x <= player.x and enemy.y <= player.y:
                enemy.move(enemy_vel, enemy_vel) # Move down and right
                if enemy.get_direction() == "LEFT":
                    enemy.flip()
                enemy.set_direction("RIGHT")
            if enemy.x <= player.x and enemy.y >= player.y:
                enemy.move(enemy_vel, -enemy_vel) # Move up and right
                if enemy.get_direction() == "LEFT":
                    enemy.flip()
                enemy.set_direction("RIGHT")
            
            if player.x <= enemy.x <= player.x + 10 and player.y <= enemy.y <= player.y + 10:
                lives -= 1
                enemies.remove(enemy)  # Remove the enemy from existence when it makes contact with the player          
            # Remove enemy from list if an arrow hits an enemy
                # enemies.remove(enemy)
                
main()