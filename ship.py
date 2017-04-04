import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

	def __init__(self,ai_settings,screen):
		super().__init__()
		"""初始化飞船位置"""
		self.screen=screen
		self.ai_settings=ai_settings

		# 加载图像获取外接矩形
		self.image=pygame.image.load('images/ship.bmp')
		self.rect=self.image.get_rect()
		self.screen_rect=screen.get_rect()

		# 将新飞船放到屏幕底部中央
		self.rect.centerx=self.screen_rect.centerx
		self.rect.bottom=self.screen_rect.bottom

		# 飞船的属性center中存float
		self.center=float(self.rect.centerx)

		# 移动标志
		self.moving_right=False
		self.moving_left=False

	def update(self):
		"""根据移动标志调整飞船位置"""

		#### 这里可以尝试修改为从右移动到左
		if self.moving_right and self.rect.right < self.screen_rect.right:
			# 更新center而不是rect
			# self.rect.centerx+=1
			self.center+=self.ai_settings.ship_speed_factor
		# 不能用elif,否则左移会失效
		if self.moving_left and self.rect.left > 0:
			self.center-=self.ai_settings.ship_speed_factor

		# 因为rect的centerx只能存整数
		# 根据self.center更新rect
		self.rect.centerx=self.center

	def blitme(self):
		"""指定位置绘制飞船"""
		self.screen.blit(self.image,self.rect)

	def center_ship(self):
		self.center=self.screen_rect.centerx