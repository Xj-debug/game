import math
import traceback

from random import randint, choice
import pygame
import sys
from pygame.locals import *

class Ball(pygame.sprite.Sprite):
    def __init__(self,glayball_image,greenball_image,position,speed,target,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.glayball_image = pygame.image.load(glayball_image).convert_alpha()
        self.greenball_image = pygame.image.load(greenball_image).convert_alpha()
        self.rect = self.glayball_image.get_rect()
        self.rect.left, self.rect.top = position
        self.side = [choice([-1,1]),choice([-1,1])]
        self.speed = speed
        self.collide = False
        self.target = target
        self.control = False
        self.width ,self.height = bg_size[0], bg_size[1]
        self.radius = self.rect.width / 2

    def move(self):
        if self.control:
            self.rect = self.rect.move(self.speed)
        else:
            self.rect = self.rect.move((self.side[0] * self.speed[0], \
                                   self.side[1] * self.speed[1]))

        if self.rect.right <= 0:
            self.rect.left = self.width

        elif self.rect.left >= self.width:
            self.rect.right = 0
        elif self.rect.bottom <= 0:
            self.rect.top = self.height
        elif self.rect.top >= self.height:
            self.rect.bottom = 0

    def check(self,motion):
        if self.target < motion < self.target+8:
            self.control = True
            return True

        else:
            return False


class Glass():
    def __init__(self,glass_image,mouse_image,bg_size):
        self.glass_image = pygame.image.load(glass_image).convert_alpha()
        self.glass_rect = self.glass_image.get_rect()
        self.glass_rect.left, self.glass_rect.top = \
                            (bg_size[0] - self.glass_rect.width) // 2, \
                            bg_size[1] - self.glass_rect.height

        self.mouse_image = pygame.image.load('hand.png')
        self.mouse_rect = self.mouse_image.get_rect()
        self.mouse_rect.left, self.mouse_rect.top = \
                              self.glass_rect.left,self.glass_rect.top
        pygame.mouse.set_visible(False)




def main():
    pygame.init()

    glayball_image = 'glayball_image.png'
    greenball_image = 'greenball_image.png'
    bg_image = 'background.png'
    glass_image = 'glass_image.png'
    mouse_image = pygame.image.load('hand.png')
    holes_image = pygame.image.load('holes_image.png')


    running = True

    #添加背景音乐
    pygame.mixer.music.load('background1.wav')
    pygame.mixer.music.play()

    #loser_sound = pygame.mixer.Sound('loser_sound.wav')
    winner_sound = pygame.mixer.Sound('bg1(0).wav')
    holes_sound = pygame.mixer.Sound('holes.wav')


    Gameover = USEREVENT
    pygame.mixer.music.set_endevent(Gameover)


    #根据背景图片指定游戏界面尺寸
    bg_size = width, height = 1024, 681
    screen = pygame.display.set_mode((bg_size))
    pygame.display.set_caption(' Play the ball')
    background = pygame.image.load(bg_image)

    holes = [(117,119,199,201),(225,227,390,392), \
             (503,505,320,322),(698,700,192,194),(906,908,419,421)]
    hole_number = 5

    balls = []
    group = pygame.sprite.Group()
    BAL_NUM = 5


    for i in range(BAL_NUM):
        position = randint(0,width-100), randint(0,height-100)
        speed = [randint(1,10), randint(1,10)]
        ball = Ball(glayball_image,greenball_image, position, speed,3*(BAL_NUM+i),bg_size)
        while pygame.sprite.spritecollide(ball,group,False,pygame.sprite.collide_circle):
            ball.rect.left, ball.rect.top = randint(0, width - 100), randint(0, height - 100)
        balls.append(ball)
        group.add(ball)

    glass = Glass(glass_image,mouse_image,bg_size)


    #鼠标在玻璃面板移动的次数
    motion = 0

    MYTIMER = USEREVENT + 1
    pygame.time.set_timer(MYTIMER,1000)

    pygame.key.set_repeat(100,100)

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



            elif event.type == MYTIMER:
                if motion:
                    for each in group:
                        if each.check(motion):
                            each.speed = [0,0]
                            each.control = True
                    motion = 0

            elif event.type == MOUSEMOTION:
                motion += 1

            elif event.type == KEYDOWN:
                if event.key == K_w:
                    for each in group:
                        if each.control:
                            each.speed[1] -= 1

                if event.key == K_s:
                    for each in group:
                        if each.control:
                            each.speed[1] += 1

                if event.key == K_a:
                    for each in group:
                        if each.control:
                            each.speed[0] -= 1

                if event.key == K_d:
                    for each in group:
                        if each.control:
                            each.speed[0] += 1

                if event.key == K_SPACE:
                    for each in group:
                        if each.control:
                            for i in holes:
                                if i[0]-5 <= each.rect.left <= i[1]+5 and i[2]-5 <= each.rect.top <= i[3]+5:

                                    holes_sound.play()
                                    each.speed = [0,0]
                                    group.remove(each)
                                    temp = balls.pop(balls.index(each))
                                    balls.insert(0,temp)
                                    holes.remove(i)
                                    hole_number -= 1
                            if not holes:
                                pygame.mixer.music.stop()
                                winner_sound.play()
                                pygame.time.delay(3000)

                                    



        screen.blit(background,(0,0))
        screen.blit(glass.glass_image, glass.glass_rect)
        for i in range(hole_number):
            screen.blit(holes_image,(holes[i][0],holes[i][2]))


        glass.mouse_rect.left, glass.mouse_rect.top = pygame.mouse.get_pos()
        if glass.mouse_rect.left < glass.glass_rect.left:
            glass.mouse_rect.left = glass.glass_rect.left

        if glass.mouse_rect.left > glass.glass_rect.right-glass.mouse_rect.width:
            glass.mouse_rect.left = glass.glass_rect.right-glass.mouse_rect.width

        if glass.mouse_rect.top < glass.glass_rect.top:

            glass.mouse_rect.top = glass.glass_rect.top

        if glass.mouse_rect.top > glass.glass_rect.bottom - glass.mouse_rect.height:
            glass.mouse_rect.top = glass.glass_rect.bottom - glass.mouse_rect.height

        screen.blit(glass.mouse_image, glass.mouse_rect)

        for each in balls:
            each.move()
            if each.collide:
                each.speed = [randint(1,10),randint(1,10)]
                each.collide = False
            if each.control:
                screen.blit(each.greenball_image,each.rect)
            else:
                screen.blit(each.glayball_image, each.rect)

        for each in group:
            group.remove(each)
            if pygame.sprite.spritecollide(each,group,False,pygame.sprite.collide_circle):
                each.side[0] = -each.side[0]
                each.side[1] = -each.side[1]
                each.collide = True
                if each.control:
                    each.side[0] = -1
                    each.side[1] = -1
                    each.control = False

            group.add(each)

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except :
        traceback.print_exc()
        pygame.quit()
        input()



