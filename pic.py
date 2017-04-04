# 死循环不要用这个py

import pygame

class S():
	def __init__(self,screen):
		self.image=pygame.image.load('images/ship.bmp')
		self.rect=self.image.get_rect()

		self.rect.center=screen.get_rect().center

pygame.init()

screen=pygame.display.set_mode((1200,800))

s=S(screen)

while True:

	screen.fill((0,0,255))

	screen.blit(s.image,s.rect)

	pygame.display.flip()
