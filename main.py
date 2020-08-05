# Created by Asif Ally 
# www.asifally.com
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
ARROW_IMG = pygame.image.load(os.path.join("assets", "player_arrow.png"))
ENEMY_IMG = pygame.image.load(os.path.join("assets", "enemy_img.png"))
ENEMY_ARROW_IMG = pygame.image.load(os.path.join("assets", "enemy_arrow.png"))
# Background image
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.png")), (WIDTH, HEIGHT))

class Character():
    COOLDOWN = 30 # Half a second
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.character_img = None
        self.arrow_img = None
        self.arrows_right = []
        self.arrows_left = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.character_img, (self.x, self.y))
        for arrow in self.arrows_right:
            arrow.draw(window)
        for arrow in self.arrows_left:
            arrow.draw(window)

    def move_arrows_right(self, vel, obj):
        self.cooldown()
        for arrow in self.arrows_right:
            arrow.move(vel)
            if arrow.off_screen(WIDTH, HEIGHT):
                self.arrows_right.remove(arrow)
            elif arrow.collision(obj):
                obj.health -= 10
                self.arrows_right.remove(arrow)
    def move_arrows_left(self, vel, obj):
        self.cooldown()
        for arrow in self.arrows_left:
            arrow.move(vel)
            if arrow.off_screen(WIDTH, HEIGHT):
                self.arrows_left.remove(arrow)
            elif arrow.collision(obj):
                obj.health -= 10
                self.arrows_left.remove(arrow)

    def cooldown(self):
        # If counter is greater than half a second
        if self.cool_down_counter >= self.COOLDOWN:
            # Set the counter to 0
            self.cool_down_counter = 0
        # If the counter is greater than 0
        elif self.cool_down_counter > 0:
            # Increment it
            self.cool_down_counter += 1

    def shoot_right(self):
        if self.cool_down_counter == 0:
            arrow = Arrow(self.x, self.y, self.arrow_img)
            self.arrows_right.append(arrow)
            self.cool_down_counter = 1
    def shoot_left(self):
        if self.cool_down_counter == 0:
            arrow = Arrow(self.x, self.y, self.arrow_img)
            self.arrows_left.append(arrow)
            self.cool_down_counter = 1
    def flip_arrow(self):
        self.arrow_img = pygame.transform.flip(self.arrow_img, True, False)

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
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, xvel):
        self.x += xvel
    
    def off_screen(self, width, height):
        return not(0 <= self.x <= width and 0 <= self.y <= height)

    def collision(self, obj):
        return collide(obj, self)

def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None # Returns (x, y)

class Enemy(Character):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.character_img = ENEMY_IMG
        self.mask = pygame.mask.from_surface(self.character_img)
        self.direction = ""
        self.arrow_img = ENEMY_ARROW_IMG
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
    def move_arrows_right(self, vel, objs):
        self.cooldown()
        score_incrementor = 0
        for arrow in self.arrows_right:
            arrow.move(vel)
            if arrow.off_screen(WIDTH, HEIGHT):
                self.arrows_right.remove(arrow)
            else:
                for obj in objs:
                    if arrow.collision(obj):
                        objs.remove(obj)
                        if arrow in self.arrows_right:
                            self.arrows_right.remove(arrow)
                        score_incrementor += 1
        return score_incrementor
    def move_arrows_left(self, vel, objs):
        self.cooldown()
        score_incrementor = 0
        for arrow in self.arrows_left:
            arrow.move(vel)
            if arrow.off_screen(WIDTH, HEIGHT):
                self.arrows_left.remove(arrow)
            else:
                for obj in objs:
                    if arrow.collision(obj):
                        objs.remove(obj)
                        if arrow in self.arrows_left:
                            self.arrows_left.remove(arrow)
                        score_incrementor += 1
        return score_incrementor
    
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x + self.character_img.get_width()/2, self.y + self.character_img.get_height() - 20, self.character_img.get_width()/5, 2))
        pygame.draw.rect(window, (0,255,0), (self.x + self.character_img.get_width()/2, self.y + self.character_img.get_height() - 20, (self.character_img.get_width() * (self.health/self.max_health))/5, 2))



def main():
    run = True
    FPS = 60
    lives = 3
    level = 0
    score = 0
    player_vel = 5
    clock = pygame.time.Clock()
    enemies = []
    wave_length = 5
    enemy_vel = 1
    laser_vel = 5

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
        if keys[pygame.K_a] or keys[pygame.K_LEFT] and player.x - player_vel + 50 > 0: # left
            player.x -= player_vel
            if player.get_direction() == "RIGHT":
                player.flip()
                player.flip_arrow()
            player.set_direction("LEFT")
        if keys[pygame.K_w] or keys[pygame.K_UP] and player.y - player_vel + 50 > 0: # up
            player.y -= player_vel
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() - 50 < WIDTH: # right
            player.x += player_vel
            if player.get_direction() == "LEFT":
                player.flip()
                player.flip_arrow()
            player.set_direction("RIGHT")
        if keys[pygame.K_s] or keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() - 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]: #Spacebar
            if player.get_direction() == "RIGHT":
                player.shoot_right()
            else:
                player.shoot_left()

        
        # Moving the enemies towards the player
        for enemy in enemies[:]:
            if enemy.x >= player.x and enemy.y >= player.y:
                enemy.move(-enemy_vel, -enemy_vel) # Move up and left
                if enemy.get_direction() == "RIGHT":
                    enemy.flip()
                    enemy.flip_arrow()
                enemy.set_direction("LEFT")
                enemy.move_arrows_left(-laser_vel, player)
            if enemy.x >= player.x and enemy.y <= player.y:
                enemy.move(-enemy_vel, enemy_vel) # Move down and left
                if enemy.get_direction() == "RIGHT":
                    enemy.flip()
                    enemy.flip_arrow()
                enemy.set_direction("LEFT")
                enemy.move_arrows_left(-laser_vel, player)
            if enemy.x <= player.x and enemy.y <= player.y:
                enemy.move(enemy_vel, enemy_vel) # Move down and right
                if enemy.get_direction() == "LEFT":
                    enemy.flip()
                    enemy.flip_arrow()
                enemy.set_direction("RIGHT")
                enemy.move_arrows_right(laser_vel, player)
            if enemy.x <= player.x and enemy.y >= player.y:
                enemy.move(enemy_vel, -enemy_vel) # Move up and right
                if enemy.get_direction() == "LEFT":
                    enemy.flip()
                    enemy.flip_arrow()
                enemy.set_direction("RIGHT")
                enemy.move_arrows_right(laser_vel, player)
            
            # Some enemies can shoot randomly
            if random.randrange(0, 15 * FPS) == 1:
                if enemy.get_direction() == "RIGHT":
                    enemy.shoot_right()
                else:
                    enemy.shoot_left()

            '''if player.x <= enemy.x <= player.x + 10 and player.y <= enemy.y <= player.y + 10:
                lives -= 1
                enemies.remove(enemy) ''' # Remove the enemy from existence when it makes contact with the player          
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
                if player.health <= 0:
                    lives -= 1
                    if lives >= 1:
                        player.health = 100

        score += player.move_arrows_right(laser_vel, enemies)
        score += player.move_arrows_left(-laser_vel, enemies)

def main_menu():
    run = True
    title_font = pygame.font.SysFont('comicsans', 50)
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse button to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()