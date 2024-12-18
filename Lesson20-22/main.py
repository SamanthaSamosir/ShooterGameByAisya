from pygame import *
class GameSprite(sprite.Sprite):
    # class constructor
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        # every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        # every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def get_collision_rect(self, margin=5):
        return self.rect.inflate(-margin, -margin)

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# child class for the player sprite (controlled by arrows)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


# child class for the enemy sprite (moves by itself)
class Enemy(GameSprite):
    direction = "left"
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

#obstacles
class Wall(sprite.Sprite):
    def __init__ (self, color1,color2,color3,wallX,wallY,wallWidth,wallHeight):
        super().__init__()
        self.color1=color1
        self.color2 = color2
        self.color3 = color3
        self.width=wallWidth
        self.height=wallHeight

        self.image=Surface((self.width,self.height))
        self.image.fill((color1,color2,color3))
        self.rect=self.image.get_rect()
        self.rect.x=wallX
        self.rect.y=wallY
    def drawWall(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

# Game scene:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("konoha.png"), (win_width, win_height))

# Game characters:
player = Player('Itachi.png', 5, win_height - 80, 4)
monster = Enemy('Sasuke.png', win_width - 80, 280, 2)
final = GameSprite('Kyubi.png', win_width - 120, win_height - 80, 0)

w1 = Wall(170,51,106,100,20,400,10)
w2 = Wall(170,51,106,100,20,10,370)
w3 = Wall(170,51,106,190,130,10,260)
w4 = Wall(170,51,106,190,130,200,10)
w5 = Wall(170,51,106,390,130,10,260)
w6 = Wall(170,51,106,490,20,10,150)
w7 = Wall(170,51,106,500,420,120,10)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

"""# music
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
"""
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        monster.update()

        player.reset()
        monster.reset()
        final.reset()

        w1.drawWall()
        w2.drawWall()
        w3.drawWall()
        w4.drawWall()
        w5.drawWall()
        w6.drawWall()
        w7.drawWall()

        if sprite.collide_rect(player,monster) or sprite.collide_rect(player,w1) or sprite.collide_rect(player,w2) or sprite.collide_rect(player,w3) or sprite.collide_rect(player,w4) or sprite.collide_rect(player,w5) or sprite.collide_rect(player,w6) or sprite.collide_rect(player,w7):
            finish=True
            window.blit(lose,(200,200))

        if sprite.collide_rect(player,final):
            finish=True
            window.blit(win, (200, 200))

    display.update()
    clock.tick(FPS)


