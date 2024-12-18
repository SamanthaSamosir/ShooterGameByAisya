import pygame.event
from pygame import *
from random import randint
from pygame import sprite

#music
#font
font.init()
font1 = font.Font(None,80)
winText = font1.render("You Win!", True,(255,255,255))
loseText = font1.render("You Lose!", True,(180,0,0))
font2 = font.Font(None,36)

#images
imgBg = "konoha.png"
imgPlayer = "naruto.png"
imgEnemy = "enemy.png"
imgBullet = "shuriken.png"

#variables
score = 0
lost = 0
maxLost = 3
goal = 11

#create a window
win_width = 700
win_height = 500
display.set_caption("Shuriken Game")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(imgBg), (win_width, win_height))
#class for other sprites
class GameSprite(sprite.Sprite):
    def __init__(self, playerImage, playerX, playerY, sizeX, sizeY, playerSpeed):
        sprite.Sprite.__init__(self)
        self.image=transform.scale(image.load(playerImage), (sizeX,sizeY))
        self.speed = playerSpeed
        self.rect = self.image.get_rect()
        self.rect.x = playerX
        self.rect.y = playerY
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(imgBullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        # disappears upon reaching the screen edge
        if self.rect.y < 0:
            self.kill()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        #disappear
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y=0
            lost += 1

#generate characters
player = Player(imgPlayer, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(imgEnemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

bullets = sprite.Group()

finish =False
run =True
while run:
    for e in event.get():
        if e.type == QUIT:
            run=False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fire_sound.play()
                player.fire()

    if not finish:
        window.blit(background,(0,0))

        #text
        text=font2.render("Score: "+str(score),1,(0,0,0))
        window.blit(text,(10,20))

        text_lose = font2.render("Missed: " + str(lost), 1, (0,0,0))
        window.blit(text_lose, (10, 50))

        player.update()
        monsters.update()
        bullets.update()

        player.reset()
        monsters.draw(window)
        bullets.draw(window)

        #check collision between shuriken and the enemies
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for collide in collides:
            score += 1 #score = score + 1
            monster = Enemy(imgEnemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(player,monsters,False) or lost >= maxLost:
            finish = True
            window.blit(loseText, (200, 200))
        #conditional statement for winning the game
        if score >= goal:
            #time.delay(5000)
            finish = True
            window.blit(winText, (200, 200))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        for bullet in bullets:
            bullet.kill()
        for monster in monsters:
            monster.kill()
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(imgEnemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
    time.delay(50)