#coding=utf-8
import random as rd
import pygame
class Settings():

#存储《外星人入侵》的所有设置的类

	def __init__(self):
		"""初始化游戏设置"""
		#屏幕绘制
		self.screen_width  = 600
		self.screen_height = 800
		self.bg_color = (230,230,230)

		#飞船的设置
		self.ship_speed_factor = 40	
		self.ship_limit = 3
		
		#设置子弹
		self.bullet_speed_factor = 50
		self.bullet_width = 5
		self.bullet_height = 9
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 100

		#外星人设置
		self.alien_speed_factor = 5
		self.fleet_drop_speed = 10
		
		#fleet_direction 为1表示向右移动，为-1表示向左移动
		self.fleet_direction = 1 
