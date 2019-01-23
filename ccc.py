import pygame
import math

pygame.init()

screensize1 = 800
screensize2 = 600


win = pygame.display.set_mode((screensize1, screensize2))

pygame.display.set_caption('NAVEEN')


class Player(object):
    def __init__(self, color, x, y, width, height, score):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 20
        self.score = score
        self.up = False
        self.down = False


class Projectile(object):
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.radius = 10
        self.color = (165, 135, 175)
        self.angle = angle
        self.vel = 20
        self.xvel = int(round((math.sin(math.radians(self.angle)) * self.vel), 0))
        self.yvel = int(round((math.cos(math.radians(self.angle)) * self.vel), 0))


def redraw_game_window():
    global Char2Win, Char1Win, s1_WaitToStart
    win.fill((0, 0, 0))
    pygame.draw.line(win, (255, 0, 0), (screensize1//2, 0), (screensize1//2, screensize2), 4)
    if s1_WaitToStart is True:
        win.blit(pygame.font.SysFont('None', 50).render('Press Space To Start', 0, (255, 255, 255)), ((screensize1//2)-180, ((screensize2//2)-25)))
    if Char1Win is True:
        win.blit(pygame.font.SysFont('None', 50).render('Player 1 Wins', 0, (255, 255, 255)), ((screensize1//4)-160, ((screensize2//2)-25)))
        win.blit(pygame.font.SysFont('None', 50).render('Press Space To Start New Game', 0, (255, 255, 255)), ((screensize1//2)-200, ((screensize2//4 + screensize2//2)-25)))
    if Char2Win is True:
        win.blit(pygame.font.SysFont('None', 50).render('Player 2 Wins', 0, (255, 255, 255)), ((screensize1//4 + screensize1//2)-160, ((screensize2//2)-25)))
        win.blit(pygame.font.SysFont('None', 50).render('Press Space To Start New Game', 0, (255, 255, 255)), ((screensize1//2)-200, ((screensize2//4 + screensize2//2)-25)))
    win.blit(pygame.font.SysFont('None', 100).render(str(char1.score) + '     ' + str(char2.score), 0, (255, 255, 255)), ((screensize1//2)-85, 20))
    pygame.draw.rect(win, char1.color, (char1.x, char1.y, char1.width, char1.height))
    pygame.draw.rect(win, char2.color, (char2.x, char2.y, char2.width, char2.height))
    pygame.draw.circle(win, ball.color, (ball.x, ball.y), ball.radius)
    pygame.display.update()


char1 = Player((255, 0, 0), 25, (screensize2//2) - 90, 25, 160, 0)
char2 = Player((255, 0, 0), screensize1 - 50, (screensize2//2) - 90, 25, 160, 0)
ball = Projectile((screensize1//8) + (screensize1//4), screensize2//4, 315)

s1_WaitToStart = True
s2_BallAtPlayerOne = False
s3_PlayerTwoScore = False
s4_PlayerOneHit = False
s5_HitsWall = False
s6_BallAtPlayerTwo = False
s7_PlayerOneScore = False
s8_PlayerTwoHit = False

Char1Win = False
Char2Win = False
laststate = ''


run = True
while run:
    pygame.time.delay(2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_r] and char1.y > char1.vel:
        char1.y -= char1.vel
    if keys[pygame.K_f] and char1.y < screensize2 - char1.height - char1.vel:
        char1.y += char1.vel

    if keys[pygame.K_UP] and char2.y > char2.vel:
        char2.y -= char2.vel
    if keys[pygame.K_DOWN] and char2.y < screensize2 - char2.height - char2.vel:
        char2.y += char2.vel

# STATES OF GAME PLAY *************************************************************************************************

    if s1_WaitToStart is True:
        ball.x = (screensize1//8) + (screensize1//4)
        ball.y = screensize2//4
        if keys[pygame.K_SPACE]:
            s2_BallAtPlayerOne = True
            s1_WaitToStart = False

    if s1_WaitToStart is False and s7_PlayerOneScore is False and s3_PlayerTwoScore is False and s4_PlayerOneHit is False and s8_PlayerTwoHit is False and s5_HitsWall is False:
        ball.x += ball.xvel
        ball.y += ball.yvel

    if s2_BallAtPlayerOne is True:
        ball.xvel = int(round((math.sin(math.radians(ball.angle)) * ball.vel), 0))
        ball.yvel = int(round((math.cos(math.radians(ball.angle)) * ball.vel), 0))
        if ball.x <= char1.x + char1.width:
            if char1.y - (2 * ball.radius) < ball.y or ball.y < char1.y + char1.height:
                s4_PlayerOneHit = True
                s2_BallAtPlayerOne = False
        if ball.x < char1.x + char1.width + ball.radius:
            if char1.y + char1.height + ball.radius <= ball.y or ball.y <= char1.y - ball.radius:
                s3_PlayerTwoScore = True
                s2_BallAtPlayerOne = False
        if ball.y >= screensize2 - (2 * ball.radius):
            if laststate != 's5':
                s5_HitsWall = True
                s2_BallAtPlayerOne = False
        if ball.y <= 0 + (2 * ball.radius):
            if laststate != 's5':
                s5_HitsWall = True
                s2_BallAtPlayerOne = False
        laststate = 's2'

    if s3_PlayerTwoScore is True:
        char2.score += 1
        if char2.score == 5:
            Char2Win = True
            s3_PlayerTwoScore = False
        ball.x = (screensize1 // 8) + (screensize1 // 2)
        ball.y = screensize2 // 4
        ball.angle = 315
        s2_BallAtPlayerOne = True
        s3_PlayerTwoScore = False
        laststate = 's3'

    if s4_PlayerOneHit is True:
        ball.xvel = 0
        ball.yvel = 0
        if 0 < ball.angle > 270:
            ball.angle -= 270
            ball.x += ball.xvel
            ball.y += ball.yvel
            s6_BallAtPlayerTwo = True
            s4_PlayerOneHit = False
        elif 270 > ball.angle > 180:
            ball.angle -= 90
            ball.x += ball.xvel
            ball.y += ball.yvel
            s6_BallAtPlayerTwo = True
            s4_PlayerOneHit = False
        laststate = 's4'

    if s5_HitsWall is True:
        ball.xvel = 0
        ball.yvel = 0
        if ball.y < screensize2//2:
            if 180 > ball.angle > 90:
                ball.angle -= 90
                s6_BallAtPlayerTwo = True
                s5_HitsWall = False
            else:
                ball.angle += 90
                s2_BallAtPlayerOne = True
                s5_HitsWall = False
        if ball.y > screensize2//2:
            if 0 < ball.angle < 90:
                ball.angle += 90
                s6_BallAtPlayerTwo = True
                s5_HitsWall = False
            else:
                ball.angle -= 90
                s2_BallAtPlayerOne = True
                s5_HitsWall = False
        laststate = 's5'

    if s6_BallAtPlayerTwo is True:
        ball.xvel = int(round((math.sin(math.radians(ball.angle)) * ball.vel), 0))
        ball.yvel = int(round((math.cos(math.radians(ball.angle)) * ball.vel), 0))
        if ball.x >= char2.x - (2 * ball.radius):
            if char2.y - (2 * ball.radius) < ball.y or ball.y < char2.y + char2.height + ball.y:
                s8_PlayerTwoHit = True
                s6_BallAtPlayerTwo = False
        if ball.x > char2.x - (2 * ball.radius):
            if char2.y + char2.height <= ball.y or ball.y <= char2.y - (2 * ball.radius):
                s7_PlayerOneScore = True
                s6_BallAtPlayerTwo = False
        if ball.y >= screensize2 - (2 * ball.radius):
            if laststate != 's5':
                s5_HitsWall = True
                s6_BallAtPlayerTwo = False
        if ball.y <= 0 + (2 * ball.radius):
            if laststate != 's5':
                s5_HitsWall = True
                s6_BallAtPlayerTwo = False
        laststate = 's6'

    if s7_PlayerOneScore is True:
        char1.score += 1
        if char1.score == 4:
            Char1Win = True
            s7_PlayerOneScore = False
        ball.x = (screensize1 // 8) + (screensize1 // 4)
        ball.y = screensize2 // 4
        ball.angle = 45
        s6_BallAtPlayerTwo = True
        s7_PlayerOneScore = False
        laststate = 's7'

    if s8_PlayerTwoHit is True:
        ball.xvel = 0
        ball.yvel = 0
        if 0 < ball.angle < 90:
            ball.angle += 270
            ball.x += ball.xvel
            ball.y += ball.yvel
            s2_BallAtPlayerOne = True
            s8_PlayerTwoHit = False
        elif 90 < ball.angle < 180:
            ball.angle += 90
            ball.x += ball.xvel
            ball.y += ball.yvel
            s2_BallAtPlayerOne = True
            s8_PlayerTwoHit = False
        laststate = 's8'

    if Char2Win is True:
        ball.xvel = 0
        ball.yvel = 0
        ball.x = (screensize1 // 8) + (screensize1 // 4)
        ball.y = screensize2 // 4
        if keys[pygame.K_SPACE]:
            char2.score = 0
            char1.score = 0
            Char2Win = False
            s1_WaitToStart = True

    if Char1Win is True:
        ball.xvel = 0
        ball.yvel = 0
        ball.x = (screensize1 // 8) + (screensize1 // 4)
        ball.y = screensize2 // 4
        if keys[pygame.K_SPACE]:
            char2.score = 0
            char1.score = 0
            Char1Win = False
            s1_WaitToStart = True

    redraw_game_window()

pygame.quit()