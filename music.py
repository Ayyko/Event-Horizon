import pygame, sys, time, random

pygame.init()

WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)

def music():
    pickUpSound = pygame.mixer.Sound('pickup.wav')
    pygame.mixer.music.load('music/Data Transfer.wav')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.queue('music/08 Dimethyltriptamine.mp3')
    pygame.mixer.music.play(-1, 0.0)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

music()
