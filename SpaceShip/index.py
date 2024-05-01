import pygame, random
 
WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceShip")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont('serif', size)
    text_surface = font.render(text, True, WHITE) 
    text_rect  = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shield_bar(surface , x, y, percentage):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage/150)*BAR_LENGTH
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        jugador_image = pygame.image.load("assets/jugador.png").convert()
        self.image = pygame.transform.scale(jugador_image, (60 , 60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT -10
        self.speed_x = 0
        self.shield = 150


    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate [pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right >WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/meteorGrey_med2.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,20)
        self.speedx = random.randrange(-5,5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if (self.rect.top > HEIGHT + 10) or (self.rect.left < - 25) or (self.rect.right > WIDTH + 25):
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = 0
            self.speedy = random.randrange(1,7)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemigo_image =   pygame.image.load("assets/enemigo.png").convert()
        self.image = pygame.transform.scale(enemigo_image, (60, 60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = 0
        self.speedy = random.randrange(1,7)
        self.speedx = random.randrange(-5,5)

    def update(self):
        inGame = 0
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx *= -1  

        if self.rect.top < 0 or self.rect.bottom > HEIGHT-100:
            self.speedy *= -1
    
    def shoot(self):
        bullet2 = Bullet2(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet2)
        enemy_bullets.add(bullet2)
        laser_sound.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        laser = pygame.image.load("assets/las.png").convert()
        self.image = pygame.transform.scale(laser, (14, 26 ))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Bullet2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        laser = pygame.image.load("assets/laser1.png").convert()
        self.image = pygame.transform.scale(laser, (14, 26 ))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = 4

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


fondo = pygame.image.load("assets/fondo.png")
background = pygame.transform.scale(fondo, (WIDTH, HEIGHT))

laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")

all_sprites = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
bullets    = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

enemyList = []

enemies = 4

player = Player()
all_sprites.add(player)
for i in range(enemies):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)
    enemy = Enemy()
    all_sprites.add(enemy)
    enemy_list.add(enemy)
    enemyList.append(enemy)

score = 0

running= True
while running:
    clock.tick(60)
    
    if(random.randint(0, 30 ) == 5):
        enemyList[1].shoot()
    

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


    all_sprites.update()

    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        pass
        score += 10
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        explosion_sound.play()    


    hits = pygame.sprite.groupcollide(enemy_list, bullets, True, True)
    for hit in hits:
        pass
        score += 50
        explosion_sound.play( )
        enemy = Enemy()
        all_sprites.add(enemy)
        enemy_list.add(enemy)
        enemyList.append(enemy)  
        enemyList.remove(hit) 

    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 100
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        explosion_sound.play()  
        if player.shield <= 0:            
            running = False


    hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for hit in hits:
        player.shield -= 50
        if player.shield <= 0:            
            running = False
        

    screen.blit(background, [0,0])

    all_sprites.draw(screen)

    draw_text(screen, "Score: " + str(score), 20, WIDTH // 2, 10)
    
    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()  
pygame.quit()








