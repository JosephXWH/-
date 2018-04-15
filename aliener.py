#coding=utf-8
import pygame
from pygame.sprite import Sprite
import random as rd
class Alien(Sprite):

	def __init__(self, ai_settings, screen):
		"""初始化外星人并设置其初始位置"""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		#加载外星人图片，并设置其 rect 属性
		self.image= pygame.image.load('images/alien1.bmp')
		self.rect = self.image.get_rect()

		#每个外星人最初都在屏幕左上角附近
		self.rect.x = rd.randint(0,self.rect.width)
		self.rect.y = (self.rect.height - 100)

		#存储外星人的准星位置
		self.y = float(self.rect.y)
		self.x = float(self.rect.x)
	
	def blitme(self):
		"""在指定位置绘制外星人"""
		self.screen.blit(self.image, self.rect) 

	def check_edges(self):
		"""如果外星人位于边缘，就返回 True"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True

	def update(self):
		"""向左或者向右移动外星人"""	
		self.y += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.y = self.y

