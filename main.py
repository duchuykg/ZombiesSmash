import pygame, sys
from pygame import *

pygame.init()

pygame.display.set_caption("Zombies Smash")
logo = pygame.image.load(r'img\logo.webp')
bg = pygame.image.load(r'img\bg.jpg')
pygame.display.set_icon(logo)
screen = pygame.display.set_mode((1200, 673))
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        screen.blit(bg,(0,0))
        pygame.display.update()
