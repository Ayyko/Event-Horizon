import pygame, sys, time, random
from math import *
from pygame.locals import *


class Player:
    """
    Player functions, such as movement, boundary collision, health, etc
    """
    def __init__(self):
        self.pImg = pygame.image.load('images/Player1.png')
        self.pRect = self.pImg.get_rect()
        self.pRect.center = (640, 360)  # Initial pos
        self.pAngle = 0  # Initial angle
        self.pSpeed = 3.25
        self.health = 25
        self.isInvincible = False

    def move(self, direction):
        """
        Player movement
        :param direction: direction of movement (str)
        """
        if direction == 'left' and self.pRect.left > 0:
            self.pRect.move_ip(-1 * self.pSpeed, 0)
        elif direction == 'right' and self.pRect.right < 1280:
            self.pRect.move_ip(self.pSpeed, 0)
        elif direction == 'up' and self.pRect.top > 0:
            self.pRect.move_ip(0, -1 * self.pSpeed)
        elif direction == 'down' and self.pRect.bottom < 720:
            self.pRect.move_ip(0, self.pSpeed)

    def rotate(self, direction):
        """
        Rotate the sprite
        :param direction: Direction of rotation (str)
        """
        self.pAngle *= -1
        if direction == 'left':
            angleChange = 90
        elif direction == 'up':
            angleChange = 0
        elif direction == 'down':
            angleChange = 180
        else:
            angleChange = -90
        tempAng = self.pAngle + angleChange
        self.pAngle = angleChange
        self.pImg = pygame.transform.rotate(self.pImg, tempAng)

    def drawSelf(self, surface, dir):
        if not self.isInvincible:
            self.pImg = pygame.image.load('images/Player1.png')
        else:
            self.pImg = pygame.image.load('images/Player1Invin.png')
        if dir == 'left':
            angle = 90
        elif dir == 'up':
            angle = 0
        elif dir == 'down':
            angle = 180
        else:
            angle = -90

        self.pImg = pygame.transform.rotate(self.pImg, angle)
        # tempPos = self.pRect.center
        # self.pRect = self.pImg.get_rect()
        # self.pRect.center = tempPos
        surface.blit(self.pImg, self.pRect)
