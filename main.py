from pygame import *
import random

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(img), (width, height))
        self.width = width
        self.height = height
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update_l(self, block):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > block:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - block - self.height:
            self.rect.y += self.speed
    def update_r(self, block):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > block:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - block-self.height:
            self.rect.y += self.speed
class Ball(GameSprite):
    def update(self, step):
        while self.speed_x == 0 or self.speed_y == 0:
            self.speed_x = random.randint(-step, step)
            self.speed_y = random.randint(-step, step)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

game = True
finish = False
background = (0, 0, 0)
win_width = 1024
win_height = 768
player_step = 16
ball_step = 8
border_step = 16
player_size_x = 32
player_size_y = 256
ball_size = 64
win = display.set_mode((win_width, win_height))
display.set_caption("Ping Pong")
clock = time.Clock()

Player_L = Player("Resources/Platform.png", player_size_x, (win_height-player_size_y)/2, player_step, player_size_x, player_size_y)
Player_R = Player("Resources/Platform.png", win_width-player_size_x*2, (win_height-player_size_y)/2, player_step, player_size_x, player_size_y)
Square = Ball("Resources/Ball.png", win_width/2-ball_size/2, win_height/2-ball_size/2, ball_step, ball_size, ball_size)
Square.speed_x = 0
Square.speed_y = 0
font.init()
font1 = font.Font("C:\WINDOWS\FONTS\ERASMD.TTF", 40)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        Square.update(ball_step)
        Player_L.update_l(border_step)
        Player_R.update_r(border_step)
        if sprite.collide_rect(Player_L, Square) or sprite.collide_rect(Player_R, Square):
            Square.speed_x *= -1
        if Square.rect.y > win_height-ball_size or Square.rect.y < 0:
            Square.speed_y *= -1
        if Square.rect.x < 0:
            finish = True
            text_L = font1.render('Left Player Lost!', True, 1, (240, 50, 50))
            text_R = font1.render('Right Player Won!', True, 1, (50, 240, 50))
        if Square.rect.x > win_width-ball_size:
            finish = True
            text_L = font1.render('Left Player Won!', True, 1, (50, 240, 50))
            text_R = font1.render('Right Player Lost!', True, 1, (240, 50, 50))
        win.fill(background)
        Player_L.reset()
        Player_R.reset()
        Square.reset()
    else:
        win.blit(text_L, (win_width/2, win_height/2-200))
        win.blit(text_R, (win_width/2, win_height/2+200))
    
    display.update()
    clock.tick(60)