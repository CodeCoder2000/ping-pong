from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 150:
            self.rect.y += self.speed
    
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 150:
            self.rect.y += self.speed

back = (200, 255, 255)
back_img = "background.jpg"
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("PING-PONG")
background = transform.scale(image.load(back_img), (win_width, win_height))
window.fill(back)

mixer.init()
mixer.music.load("bgmusic.ogg")
mixer.music.play()
ricochet = mixer.Sound("ricochet.ogg")
loser1 = mixer.Sound("winner.ogg")
loser2 = mixer.Sound("fail.ogg")

game = True
finish = False
clock = time.Clock()
FPS = 60

player_1 = Player('racket.png', 30, 200, 4, 50, 150)
player_2 = Player('racket.png', 520, 200, 4, 50, 150)
ball = GameSprite('pingpongball.png', 200, 200, 4, 50, 50)

font.init()
font = font.Font(None, 35)
lose1 = font.render('Player 1 lose', True, (255, 255 ,0))
lose2 = font.render('Player 2 lose', True, (255, 255 ,0))

speed_x = 3
speed_y = 3

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish != True:
        window.fill(back)
        window.blit(background, (0, 0))
        player_1.update_r()
        player_2.update_l()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(player_1, ball) or sprite.collide_rect(player_2, ball):
            speed_x *= -1
            speed_y *= 1
            ricochet.play()

        if ball.rect.y > win_height - 50 or ball.rect.y < 0:
            speed_y *= -1
            ricochet.play()
        
        if ball.rect.x < 0:
            mixer.music.stop()
            loser1.play()
            finish = True
            window.blit(lose1, (200, 200))
            game_over = True
        
        if ball.rect.x > win_width:
            mixer.music.stop()
            loser2.play()
            finish = True
            window.blit(lose2, (200, 200))
            game_over = True

        player_1.reset()
        player_2.reset()
        ball.reset()
    
    display.update()
    clock.tick(FPS)