import pygame


class Projectile:

    def __init__(self, pos, direction, size='small'):
        """
        Creates and moves a projectile
        :param pos = initial position (tuple)
        :param direction = direction of fire (str)
        """
        self.xVel = 0
        self.yVel = 0
        if size == 'large':
            self.shotImg = pygame.image.load('images/shotLarge.png')
        else:
            self.shotImg = pygame.image.load('images/shot.png')
        self.shotRect = self.shotImg.get_rect()
        self.shotRect.center = pos
        self.pos = self.shotRect.center
        self.xMax = self.pos[0]
        self.yMax = self.pos[1]
        self.xMaxCalc = self.pos[0]
        self.yMaxCalc = self.pos[1]
        if direction == 'up':
            self.yVel = -10
            self.yMax = self.yMaxCalc - 100
        elif direction == 'down':
            self.yVel = 10
            self.yMax = self.yMaxCalc + 100
        elif direction == 'left':
            self.xVel = -10
            self.xMax = self.xMaxCalc - 100
        else:
            self.xVel = 10
            self.xMax = self.xMaxCalc + 100
                
    def drawSelf(self, surface):
        surface.blit(self.shotImg, self.shotRect)

    def moveSelf(self):
        self.shotRect.center = (self.shotRect.center[0] + self.xVel, self.shotRect.center[1] + self.yVel)

    def isOffScreen(self):
        if self.shotRect.left <= 0:        # Projectile is off left
            return True
        elif self.shotRect.right >= 1280:  # Projectile is off right
            return True
        if self.shotRect.top <= 0:         # Projectile is off top
            return True
        elif self.shotRect.bottom >= 720:  # Projectile is off bottom
            return True
        return False
