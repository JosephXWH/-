#coding=utf-8
import sys
import pygame
import game_functions as gf
from settings import Settings
from ship import *
from pygame.sprite import Group
from bullet import Bullet as bl
from aliener import Alien
from game_stats import GameStats
from button import Button

def run_game():
	#初始化游戏并创建一个屏幕对象
	pygame.init()
	
	#引入变量ai_settings
	ai_settings = Settings()
	#使用属性值创建屏幕
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")

	#创建 Play 按钮
	play_button = Button(ai_settings, screen, "Play")
	#创建一个用于统计游戏数据的实例
	stats = GameStats(ai_settings)
	#创建一艘飞船，一个子弹编组和一个外外星人编组
	#创建一艘飞船
	ship = Ship(ai_settings,screen)
	#创建一个用于存储子弹的编组
	bullets = Group()
	#创建一个外星人
	aliens = Group()

	#创建外星人群
	gf.create_fleet(ai_settings,screen,ship,aliens)

	#设置背景色,对象 bg_color
	bg_color = (ai_settings.bg_color)

	#开始游戏主循环
	while True:
		
		#监视鼠标和键盘,使用模块game_functions()
		gf.check_events(ai_settings,screen,stats,play_button, ship,bullets)
		gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings,screen,ship, aliens, bullets)
			#每次循环时重绘屏幕,调用方法，对对象进行方法
			gf.update_aliens(ai_settings,stats,screen, ship, aliens, bullets)
		
		gf.update_screen(ai_settings,screen,stats, ship,aliens,bullets, play_button)
		"""gf.check_alien_overlap(ai_settings, aliens)"""
		#让最近绘制的屏幕可见
		pygame.display.flip()

run_game()