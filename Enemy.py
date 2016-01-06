import pygame
import random

__author__ = 'Nate Rhinehardt'


class Enemy:
    """The class responsible for the AI of the standard enemy."""

    def __init__(self, ePos, player, surface):
        """Creates an enemy with an initial position ePos, Player reference player,
            and pygame surface for initial draw."""

        self.eImg1 = pygame.image.load('images/pirate crew member.png')  # Enemy image
        self.eImg2 = pygame.image.load('images/pirate crew member2.png')
        self.eImg3 = pygame.image.load('images/pirate crew member3.png')
        self.eImg4 = pygame.image.load('images/pirate crew member4.png')
        self.eImglist = [self.eImg1, self.eImg2, self.eImg3, self.eImg4]
        self.eImg = random.choice(self.eImglist)
        self.eRect = self.eImg.get_rect()

        self.eRect.center = ePos  # Initial position

        self.pRect = player.pRect   # Sets player reference for access later.
        # Python does pass-by-reference, so this reference is updated whenever the original is
        randChoice=random.randint(0,1)
        if randChoice==0:
            self.offSet=20
        else:
            self.offSet=-20
        randChoice=random.randint(0,1)
        if randChoice==0:
            self.axis='x'
        else:
            self.axis='y'

        self.eAngle = 0     # Initial face direction is up

        # Sets velocity to 1 for each axis of movement
        self.xVel = 2.5
        self.yVel = 2.5

        # Initial rotate to player and draw
        self.eRotate(self.findDirection)
        self.drawSelf(surface)

    def drawSelf(self, surface):
        """Takes the pygame surface and blits the enemy image onto the canvas."""

        surface.blit(self.eImg, self.eRect)

    def eRotate(self, direction):
        """Takes the a direction in the form of String and changes the orientation of the enemy image."""

        self.eAngle *= -1
        if direction == 'xNeg':     # Rotates to face left
            angleChange = 90
        elif direction == 'yNeg':   # Rotates to face up
            angleChange = 0
        elif direction == 'yPos':   # Rotates to face down
            angleChange = 180
        else:                       # Rotates to face right
            angleChange = -90
        tempAng = self.eAngle + angleChange
        self.eAngle = angleChange
        self.eImg = pygame.transform.rotate(self.eImg, tempAng)
        tempPos = self.eRect.center
        self.eRect = self.eImg.get_rect()
        self.eRect.center = tempPos

    def eMove(self):
        """Moves the enemy in the direction of the player, checking if the enemy is off screen and adjusting if so."""

        # Sets the values below to handy shortcuts
        x1 = self.eRect.center[0]
        y1 = self.eRect.center[1]
        x2 = self.pRect.center[0]
        y2 = self.pRect.center[1]
        if self.axis=='x':
            x2+=self.offSet
        else:
            y2+=self.offSet

        # Resets enemy vel to 0. Breaks if we remove, don't know why.
        self.xVel = 2.5
        self.yVel = 2.5

        # This is to try to keep the enemies from conglomerating
        randAdd = random.randint(0, 1)
        if randAdd % 2 == 0:
            self.xVel += 1
        else:
            self.yVel += 1

        # Figures out if the player is up or down and left or right of the enemy and sets velocity accordingly
        if x2 > x1:     # Player is right
            self.xVel = self.xVel
        elif x2 < x1:   # Player is left
            self.xVel = -self.xVel
        else:           # Player is on same X
            self.xVel = 0
        if y2 > y1:     # Player is down
            self.yVel = self.yVel
        elif y2 < y1:   # Player is up
            self.yVel = -self.yVel
        else:           # Player is on same Y
            self.yVel = 0
        self.eRect.center = (int(x1 + self.xVel), int(y1 + self.yVel))

        # Map boundary collision
        if self.eRect.left <= 0:        # Enemy is off left
            self.eRect.center = (20, self.eRect.center[1])
        elif self.eRect.right >= 1280:  # Enemy is off right
            self.eRect.center = (1260, self.eRect.center[1])
        if self.eRect.top <= 0:         # Enemy is off top
            self.eRect.center = (self.eRect.center[0], 16)
        elif self.eRect.bottom >= 720:  # Enemy is off bottom
            self.eRect.center = (self.eRect.center[0], 704)

        self.eRotate(self.findDirection())

    def findDirection(self):
        """This method finds the longest axis to the player from its location and rotates enemy to face that.
            Returns the axis with sign as a string."""

        # Nice shortcut variables
        x1 = self.eRect.center[0]
        y1 = self.eRect.center[1]
        x2 = self.pRect.center[0]
        y2 = self.pRect.center[1]

        # Finds longest axis and sign of each
        lenX = abs(x2 - x1)
        lenY = abs(y2 - y1)
        isXPos = (x2 - x1) >= 0
        isYPos = (y2 - y1) >= 0

        if lenX > lenY and isXPos:          # Player is mostly right
            return "xPos"
        elif lenX > lenY and not isXPos:    # Player is mostly left
            return "xNeg"
        elif lenY > lenX and isYPos:        # Player is mostly down
            return "yPos"
        else:                               # Player is mostly up
            return "yNeg"

