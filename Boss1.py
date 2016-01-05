import pygame

__author__ = 'Nate Rhinehardt'


class Boss1:
    """The class responsible for the Boss AI"""

    def __init__(self):
        """Creates a boss at center of the screen"""

        self.bossImg = pygame.image.load('images/first mate boss.png')      # Boss image
        self.bossRect = self.bossImg.get_rect()

        self.bossRect.center = (240, 360)
        self.bossAngle = 0

        # Boss initial velocities for each axis
        self.xVel = 1
        self.yVel = 1


    def drawSelf(self, surface):
        """ Accepts pygame surface parameter to blit self onto canvas"""

        surface.blit(self.bossImg, self.bossRect)


    def moveSelf(self, player):
        """The method accepts a player argument to pass to the findDirection method.
            Otherwise will move the boss in a regular pattern"""

        self.bossRect.center = (self.bossRect.center[0] + self.xVel, self.bossRect.center[1] + self.yVel)

        # Map boundary collision
        if self.bossRect.left <= 0:        # Enemy is off left
            self.bossRect.center = (20, self.bossRect.center[1])
        elif self.bossRect.right >= 1280:  # Enemy is off right
            self.bossRect.center = (1260, self.bossRect.center[1])
        if self.bossRect.top <= 0:         # Enemy is off top
            self.bossRect.center = (self.bossRect.center[0], 16)
        elif self.bossRect.bottom >= 720:  # Enemy is off bottom
            self.bossRect.center = (self.bossRect.center[0], 704)

        self.bossRotate(self.findDirection(player))


    def findDirection(self, player):
        """Finds the direction to the player and returns the proper signed axis in the form of a String"""

        # Nice shortcut variables
        pRect = player.pRect
        x1 = self.bossRect.center[0]
        y1 = self.bossRect.center[1]
        x2 = pRect.center[0]
        y2 = pRect.center[1]

        # Finds the longest axis and the signs of the axes to the player
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


    def bossRotate(self, direction):
        """Rotates the image to face the player based on the String direction given by findDirection"""

        self.bossAngle *= -1
        if direction == 'xNeg':     # Face Left
            angleChange = 90
        elif direction == 'yNeg':   # Face Up
            angleChange = 0
        elif direction == 'yPos':   # Face Down
            angleChange = 180
        else:                       # Face Right
            angleChange = -90

        tempAng = self.bossAngle + angleChange
        self.bossAngle = angleChange
        self.bossImg = pygame.transform.rotate(self.bossImg, tempAng)


    def chargeAttack(self, player):
        """Sets the boss speed much higher then faces the player and charges."""

        # The new scary velocity
        self.xVel = 10
        self.yVel = 10

        # Handy shortcut variables
        x1 = self.bossRect.center[0]
        y1 = self.bossRect.center[1]
        x2 = player.pRect.center[0]
        y2 = player.pRect.center[1]

        if x2 > x1:         # Player is right
            self.xVel = self.xVel
        elif x2 < x1:       # Player is left
            self.xVel = -self.xVel
        else:               # Player is on same X
            self.xVel = 0
        if y2 > y1:         # Player is down
            self.yVel = self.yVel
        elif y2 < y1:       # Player is up
            self.yVel = -self.yVel
        else:               # Player is on same Y
            self.yVel = 0

        # Rotates and moves boss
        self.bossRotate(self.findDirection(player))
        self.bossRect.center = (int(x1 + self.xVel), int(y1 + self.yVel))

        # Resets boss speed
        self.xVel = 1
        self.yVel = 1
