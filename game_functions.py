#coding=utf-8
import sys
import pygame
from bullet import Bullet
from aliener import Alien
from time import sleep
import random as rd 
import time
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	"""相应被外星人撞到的飞船"""
	if stats.ship_left > 0:
		#将 ship_left 减1
		stats.ship_left -=1

		#清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		#创建一群新的外星人， 并将飞船放到屏幕中央
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

		#暂停
		sleep(0.5) 
	else:
		stats.game_active = False

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	"""响应按键"""
	if event.key == pygame.K_RIGHT:
		#改变标志
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)	
	elif event.key == pygame.K_q:
		sys.exit()

def check_keyup_events(event,ship,bullets):
	"""响应按键""" 
	if event.key == pygame.K_RIGHT:
		#改变标志
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False
	elif event.key == pygame.K_SPACE:
		bullets.bullet_sign = False



def check_events(ai_settings,screen,stats,play_button, ship , bullets):
	#响应按键和鼠标事件
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship,bullets)
		
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(stats, play_button, mouse_x, mouse_y)

def update_screen(ai_settings,screen, stats, ship,aliens,bullets, play_button):
	
	#更新屏幕上的图像，并切换到新屏幕
	#每次循环时都重绘屏幕
	screen.fill(ai_settings.bg_color)
	#在飞船和外星人后面重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)

	#如果游戏处于非活跃状态就绘制 button
	if not stats.game_active:
		play_button.draw_button()

	#让最近绘制的屏幕可见
	pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets):
	"""更新子弹的位置，并删除已消失的子弹"""
	#更新子弹位置
	bullets.update()
		
	#删除已经消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
	"""相应子弹和外星人的碰撞"""
	# 山出发深耕装的子弹和外星人
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if len(aliens) <= 4:
		#删除现有的子弹并新建一群外星人
		"""bullets.empty()"""
		create_fleet(ai_settings, screen, ship, aliens)

def fire_bullet(ai_settings, screen, ship, bullets):
	"""如果还没有达到限制，就在发射一颗子弹"""
	#创建一颗子弹，并将其加入编组 bullets 中
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
	"""计算每行可容纳多少外星人"""
	available_space_x = ai_settings.screen_width -  2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width) + 1)
	return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
	"""计算屏幕可以容纳多少行外星人"""
	available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height) + 1)
	return number_rows

def creat_alien(ai_settings, screen, aliens, aliens_number, row_number):
	#创建一个外星人并将其加入当前行
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = rd.randint(0,500)
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	"""创建外星人群"""
	#创建一个外星人，并确定一行容纳多少外星人
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings , alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	#创建第一行外星人
	for aliens_number in range(rd.randint(1,1)):
		row_number = 0
		creat_alien(ai_settings, screen, aliens, aliens_number, row_number)

def check_fleet_edges(ai_settings, aliens):
	"""有外星人达到边缘时采取相应措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""将整群外星人下移，并改变塔恩的方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= 1

def update_aliens(ai_settings,stats,screen, ship, aliens, bullets):
	"""检查是否有外星人位于屏幕边缘，并更新整个外星人的位置"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	#检测外新年个人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

	#检查是否有外星人到达底部
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	"""检查是否有外星人到达了底部"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 像飞机被撞倒一样镜像处理
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			break
def check_play_button(stats, play_button, mouse_x, mouse_y):
	"""在玩家单机 Play按钮是开始新游戏"""
	if play_button.rect.collidepoint(mouse_x, mouse_y):
		stats.game_active = True

"""def check_alien_overlap(ai_settings, aliens):
	for alien in aliens.sprites():
		spirte_1 = alien
		sprite_2 = alien[-1]
		result = pygame.sprite.collide_rect(sprite_1,sprite_2)"""


