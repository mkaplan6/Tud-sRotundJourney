import pygame, sys, random
from pygame import mixer

# Initialize game

pygame.init()

speed = [0, 0]

size = (width, height) = 1280, 720
screen = pygame.display.set_mode(size)

# Backdrop
class Backdrop(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./backdrop.png")
        self.image = pygame.transform.scale(self.image, (1280, 720))

        self.rect = self.image.get_rect()
        self.rect.center = (640, 360)

# Player
class MainCharacter(pygame.sprite.Sprite):
    global eaten
    eaten = 0
    global internal_eaten
    internal_eaten = 0
    # Create player sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./Tud.png")
        self.image = pygame.transform.scale(self.image, (100 + eaten, 100 + eaten))

        self.rect = self.image.get_rect()
        self.rect.center = (640, 360)

        self.last_hit = 0

    # React with objects
    def update(self):
        self.last_hit = pygame.time.get_ticks()
        updated_player = pygame.transform.scale(self.image, (100 + eaten, 100 + eaten))
        screen.blit(updated_player, (self.rect.left, self.rect.top))

# Enemies
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./bread.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, width), random.randint(0, height))

        self.speed = [3, 3]

    # AI (random)
    def update(self):
        self.rect = self.rect.move(self.speed)

        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = -self.speed[0] * 1.5
            self.speed[1] = self.speed[1] * random.uniform(0.5, 1.1)
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1] * 1.5
            self.speed[0] = self.speed[0] * random.uniform(0.5, 1.1)

        if self.speed[0] > 6:
            self.speed[0] -= 0.5
        if self.speed[0] < -6:
            self.speed[0] += 0.5

        if self.speed[1] > 6:
            self.speed[1] -= 0.5
        if self.speed[1] < -6:
            self.speed[1] += 0.5

class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./food.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, width - 50), random.randint(50, height - 50))

    def update(self):
        self.rect.center = (random.randint(50, width - 50), random.randint(50, height - 50))



# Initialize the objects
main = MainCharacter()
main_sprite = pygame.sprite.Group()
main_sprite.add(main)

enemies = pygame.sprite.Group()
enemies.add(Enemy())
enemies.add(Enemy())

food = Food()
foods = pygame.sprite.Group()
foods.add(food)

backdrop = Backdrop()
backdrops = pygame.sprite.Group()
backdrops.add(backdrop)

# Music
mixer.init()
mixer.music.load("./Jumper.wav")
mixer.music.set_volume(0.7)
mixer.music.play(-1)

# Start the game
iframes = 1000
enemyCount = 2

clock = pygame.time.Clock()
start_time = 300
while True:
    clock.tick(60)
    screen.fill((0, 0 , 0))

    # Put sprites on the screen
    backdrops.draw(screen)
    enemies.draw(screen)
    foods.draw(screen)
    main_sprite.draw(screen)
    # Display timer on the screen
    start_time -= 1

    myFont = pygame.font.SysFont("Times New Roman", 50)
    numLivesDraw = myFont.render(f"Timer: {start_time}", 1, (250, 0, 0))
    screen.blit(numLivesDraw, (30, 30))

    myFont = pygame.font.SysFont("Times New Roman", 50)
    foodConsumedDraw = myFont.render(f"Food consumed: {eaten}", 1, (250, 0, 0))
    screen.blit(foodConsumedDraw, (30, 85))

    myFont = pygame.font.SysFont("Times New Roman", 50)
    breadCountDraw = myFont.render(f"Number of Bread: {enemyCount}", 1, (250, 0, 0))
    screen.blit(breadCountDraw, (30, 125))

    myFont = pygame.font.SysFont("Times New Roman", 50)
    numLivesDraw = myFont.render(f"iFrames: {iframes}", 1, (250, 0, 0))
    screen.blit(numLivesDraw, (30, 175))


    # Player movement
    key = pygame.key.get_pressed()
    if key[pygame.K_w] and speed[1] > -20:
        speed[1] -= 1
    if key[pygame.K_a] and speed[0] > -20:
        speed[0] -= 1
    if key[pygame.K_s] and speed[1] < 20:
        speed[1] += 1
    if key[pygame.K_d] and speed[0] < 20:
        speed[0] += 1

    # Keep them in bounds
    if main.rect.left < 0 or main.rect.right > width:
        speed[0] = -speed[0] * 1.2
    if main.rect.top < 0 or main.rect.bottom > height:
        speed[1] = -speed[1] * 1.2

    # Slow down character if too fast
    if speed[0] > 0:
        speed[0] -= 0.5
    if speed[0] < 0:
        speed[0] += 0.5

    if speed[1] > 0:
        speed[1] -= 0.5
    if speed[1] < 0:
        speed[1] += 0.5

    main.rect = main.rect.move(speed)
    enemies.update()

    # Collisions with enemies
    collisionsBad = pygame.sprite.spritecollideany(main, enemies)
    if collisionsBad != None:
        interval = pygame.time.get_ticks() - main.last_hit
        if interval > iframes:
            eaten -= 1
            start_time -= 25
            main_sprite.update()
    
    collisionsFood = pygame.sprite.spritecollideany(main, foods)
    if collisionsFood != None:
        start_time += 75
        eaten += 1
        internal_eaten += 1
        #mixer.music.load("./chomp.wav")
        #mixer.music.set_volume(1)
        #mixer.music.play(1)
        food.update()
        main_sprite.update()

    # Add enemies over time and decrease iframes
    if internal_eaten % 5 == 0 and internal_eaten != 0:
        internal_eaten += 1
        enemies.add(Enemy())
        enemyCount += 1
        if iframes <= 100:
            iframes = 100
        else:
            iframes -= 100

    # Start game
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if start_time <= 0:
            print("Out of time!")
            sys.exit()