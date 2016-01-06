import pygame
import time
import random
import sys
from math import *
from pygame.locals import *
from Enemy import Enemy
from Player import Player
from Boss1 import Boss1
from Projectile import Projectile


class Game:

    def __init__(self):
        # vars
        self.winWidth = 1280
        self.winHeight = 720

        # set up window
        pygame.init()
        self.winSurface = pygame.display.set_mode((self.winWidth, self.winHeight), 0, 32)
        pygame.display.set_caption('Event Horizon')
        self.clock = pygame.time.Clock()

        self.backgroundImage = pygame.image.load('images/map.png')
        
        self.player = Player()
        self.willInvincible = False
        self.moveRight = self.moveLeft = self.moveDown = self.moveUp = self.shoot = False
        self.boss = Boss1()
        self.spawnPos = [(727, 246), (331, 129), (304, 588), (631, 588), (1135, 567), (1072, 126), (115, 96), (1198, 354), (97, 360)]
        self.heartPos = [(20,10), (50,10), (80,10), (110,10), (140,10)]
        self.allEnemies = []
        self.alive = 0
        self.pDir = 'up'
        self.maxspawn = 7
        self.breather1 = pygame.image.load('images/round1 end.png')
        self.breather2 = pygame.image.load('images/round2 end.png')
        self.breather3 = pygame.image.load('images/round3 end.png')
        self.breather4 = pygame.image.load('images/round4 end.png')
        self.breather5 = pygame.image.load('images/game end.png')

        self.allProjectiles = []

        # Splash screen stuff
        self.splash = pygame.image.load('images/splash.png')
        self.splashRect = self.splash.get_rect()
        self.winSurface.blit(self.splash, self.splashRect)
        pygame.display.update()
        time.sleep(3)

        #self.rounds(1)
        self.menu()

    def mainLoop(self, boss = 'no'):
        """This is the mainloop. It runs the game."""
        randChoice = random.randint(0, 1)
        if randChoice == 0:
            pygame.mixer.music.load('music/05 Resonance.wav')
            pygame.mixer.music.queue('music/08 Dimethyltriptamine.wav')
        else:
            pygame.mixer.music.load('music/08 Dimethyltriptamine.wav')
            pygame.mixer.music.queue('music/05 Resonance.wav')

        pygame.mixer.music.play(1, 0)

        # for i in range(self.alive):
        #     randSpawn = random.randint(0, (len(self.spawnPos)) - 1)
        #     self.allEnemies.append(Enemy(self.spawnPos[randSpawn], self.player, self.winSurface))

        FIRING = pygame.USEREVENT + 1
        INVINCIBLE = pygame.USEREVENT + 2
        fireBurst = 100
        invinTimer = 1000

        while self.alive > 0:
            if self.player.health <= 0:
                while True:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            # So python doesn't crash when you close the window
                            pygame.quit()
                            sys.exit()
                        if event.type == KEYDOWN:
                            self.menu()
                    self.winSurface.blit(pygame.image.load('images/you died.png'), (0, 0))
                    pygame.display.update()
                    self.clock.tick(30)
            if boss == 'yes':
                self.bossEnemy = Boss1()
                if self.bossDead:
                    self.alive = 0
            if self. spawns > 0 and (self.alive - self.maxspawn) < self.spawns:
                    randSpawn = random.randint(0, (len(self.spawnPos)) - 1)
                    self.allEnemies.append(Enemy(self.spawnPos[randSpawn], self.player, self.winSurface))
                    self.spawns -= 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    # So python doesn't crash when you close the window
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        pygame.time.set_timer(FIRING, fireBurst)
                        self.shoot = True

                if event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.shoot = False
                    if event.key == K_ESCAPE:
                        self.menu()

                if event.type == FIRING and self.shoot:
                    self.shoot = not self.shoot

                if event.type == INVINCIBLE:
                    self.player.isInvincible = False

                self.playerMove(event)

            if self.moveRight:
                self.player.rotate('right')
                self.player.move('right')
            if self.moveLeft:
                self.player.rotate('left')
                self.player.move('left')
            if self.moveUp:
                self.player.rotate('up')
                self.player.move('up')
            if self.moveDown:
                self.player.rotate('down')
                self.player.move('down')
            if self.shoot:
                if self.player.pAngle == 90:
                    angleChange = 'left'
                elif self.player.pAngle == 0:
                    angleChange = 'up'
                elif self.player.pAngle == 180:
                    angleChange = 'down'
                else:
                    angleChange = 'right'
                self.allProjectiles.append(Projectile(self.player.pRect.center, angleChange))

            for i in self.allProjectiles:
                i.moveSelf()

            for i in self.allEnemies:
                i.eMove()

            self.collision()
            if self.willInvincible:
                self.player.isInvincible = True
                self.willInvincible = False
                pygame.time.set_timer(INVINCIBLE, invinTimer)

            self.drawAll()

            self.clock.tick(30)


    def menu(self):
        pygame.mixer.music.load('music/Data Transfer.wav')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(1, 0)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    # So python doesn't crash when you close the window
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == ord('p'):
                        self.rounds(1)
                    if event.key == ord('e'):
                        self.rounds(-1)
                    if event.key == ord('z'):
                        self.rounds(-2)
                    if event.key == ord('q'):
                        pygame.quit()
                        sys.exit()
                    if event.key == ord('i'):
                        self.instructions()
                    if event.key == ord('c'):
                        self.credits()
            self.drawMenu()
            self.clock.tick(30)


    def instructions(self):
        pageNum=1
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    # So python doesn't crash when you close the window
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if pageNum==1:
                        pageNum=2
                    elif pageNum == 2:
                        pageNum = 3
                    else:
                        return
            self.drawInstructions(pageNum)
            self.clock.tick(30)


    def credits(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    # So python doesn't crash when you close the window
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    return
                self.drawCredits()
                self.clock.tick(30)


    def drawAll(self):

        self.winSurface.blit(self.backgroundImage, (0, 0))

        numFullHearts = self.player.health/5

        for i in range(5):
            if i<=numFullHearts-1:
                self.winSurface.blit(pygame.image.load('images/heart full.png'),self.heartPos[i])
            else:
                self.winSurface.blit(pygame.image.load('images/heart empty.png'),self.heartPos[i])

        if len(self.allProjectiles) > 0:
            for i in self.allProjectiles:
                if i.isOffScreen():
                    self.allProjectiles.remove(i)
                i.drawSelf(self.winSurface)

        for i in self.allEnemies:
            i.drawSelf(self.winSurface)

        if self.moveRight:
            self.player.rotate('right')
            self.pDir = 'right'
        if self.moveLeft:
            self.player.rotate('left')
            self.pDir = 'left'
        if self.moveUp:
            self.player.rotate('up')
            self.pDir = 'up'
        if self.moveDown:
            self.player.rotate('down')
            self.pDir = 'down'
        self.player.drawSelf(self.winSurface, self.pDir)


        pygame.display.flip()


    def drawMenu(self):
        menuImage = pygame.image.load('images/main menu.png')

        self.winSurface.blit(menuImage, (0, 0))
        pygame.display.update()


    def drawInstructions(self, page):
        if page==1:
            instImage=pygame.image.load('images/Instructions1.png')
        elif page == 2:
            instImage=pygame.image.load('images/Instructions2.png')
        else:
            instImage=pygame.image.load('images/Instructions3.png')
        self.winSurface.blit(instImage, (0,0))
        pygame.display.update()


    def drawCredits(self):
        creditsImg = pygame.image.load('images/credits3.png')
        self.winSurface.blit(creditsImg,(0,0))
        pygame.display.update()


    def playerMove(self, event):
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == ord('a'):
                self.player.rotate('left')
                self.moveRight = False
                self.moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                self.player.rotate('right')
                self.moveLeft = False
                self.moveRight = True
            if event.key == K_UP or event.key == ord('w'):
                self.player.rotate('up')
                self.moveDown = False
                self.moveUp = True
            if event.key == K_DOWN or event.key == ord('s'):
                self.player.rotate('down')
                self.moveUp = False
                self.moveDown = True

        if event.type == KEYUP:
            # if event.key == K_ESCAPE:
            #     pass  # Menu?

            if event.key == K_LEFT or event.key == ord('a'):
                self.moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                self.moveRight = False
            if event.key == K_UP or event.key == ord('w'):
                self.moveUp = False
            if event.key == K_DOWN or event.key == ord('s'):
                self.moveDown = False


    def collision(self):
        allEnemiesRect = []
        allProjRect = []

        for i in self.allEnemies:
            allEnemiesRect.append(i.eRect)
        for i in self.allProjectiles:
            allProjRect.append(i.shotRect)

        if self.player.pRect.collidelist(allEnemiesRect) is not -1 and not self.player.isInvincible:
            self.player.health -= 5
            self.willInvincible = True
            if self.player.health <= 0:
                while True:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            # So python doesn't crash when you close the window
                            pygame.quit()
                            sys.exit()
                        if event.type == KEYDOWN:
                            self.menu()
                    self.winSurface.blit(pygame.image.load('images/you died.png'), (0, 0))
                    pygame.display.update()
                    self.clock.tick(30)
        for i in self.allEnemies:
            collideProj = i.eRect.collidelist(allProjRect)
            if collideProj != -1:
                self.allEnemies.remove(i)
                self.alive -= 1
                try:
                    self.allProjectiles.remove(self.allProjectiles[collideProj])
                except IndexError:
                    print 'error!'


    def rounds(self, roundNum):

        self.player = Player()
        self.allProjectiles = []
        self.allEnemies = []
        self.moveRight = self.moveLeft = self.moveDown = self.moveUp = self.shoot = False
        if roundNum == 1:
            self.maxspawn = 7
            self.spawns = 7
            self.alive = 7
            self.mainLoop()
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        # So python doesn't crash when you close the window
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == ord('q'):
                            self.menu()
                        else:
                            self.rounds(2)
                self.winSurface.blit(self.breather1, (0, 0))
                pygame.display.update()
                self.clock.tick(30)
            self.rounds(2)
        if roundNum == 2:
            self.maxspawn = 8
            self.spawns = 14
            self.alive = 14
            self.mainLoop()
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        # So python doesn't crash when you close the window
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == ord('q'):
                            self.menu()
                        else:
                            self.rounds(3)
                self.winSurface.blit(self.breather2, (0, 0))
                pygame.display.update()
                self.clock.tick(30)
            self.rounds(3)
        if roundNum == 3:
            self.maxspawn = 9
            self.spawns = 28
            self.alive = 28
            self.mainLoop()
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        # So python doesn't crash when you close the window
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == ord('q'):
                            self.menu()
                        else:
                            self.rounds(4)
                self.winSurface.blit(self.breather3, (0, 0))
                pygame.display.update()
                self.clock.tick(30)
            self.rounds(4)
        if roundNum == 4:
            self.maxspawn = 10
            self.spawns = 56
            self.alive = 56
            self.mainLoop()
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        # So python doesn't crash when you close the window
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == ord('q'):
                            self.menu()
                        else:
                            self.rounds(5)
                self.winSurface.blit(self.breather4, (0, 0))
                pygame.display.update()
                self.clock.tick(30)
            self.rounds(5)
        if roundNum == 5:
            # self.maxspawn = 10
            # self.spawns = sys.maxint
            # self.alive = sys.maxint
            # self.mainLoop('yes')
            # while True:
            #     for event in pygame.event.get():
            #         if event.type == QUIT:
            #             # So python doesn't crash when you close the window
            #             pygame.quit()
            #             sys.exit()
            #         if event.type == KEYDOWN:
            #             if event.key == ord('q'):
            #                 self.menu()
            #             else:
            #                 self.rounds(5)
            #     self.winSurface.blit(self.breather5, (0, 0))
            #     pygame.display.update()
            #     self.clock.tick(30)
            self.menu()
        if roundNum == -1:
            self.maxspawn = 15
            self.spawns = sys.maxint
            self.alive = sys.maxint
            self.mainLoop()
            self.menu()
        if roundNum == -2:
            self.maxspawn = 0
            self.spawns = sys.maxint
            self.alive = sys.maxint
            self.mainLoop()
            self.menu()

game = Game()
