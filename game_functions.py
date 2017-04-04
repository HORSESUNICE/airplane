import sys
import pygame
from random import randint
from time import sleep

from bullet import Bullet
from alien import Alien

def check_keydown_events(event,ai_settings,screen,stats,sb,ship,aliens,bullets):
	if event.key==pygame.K_q:
		sys.exit()
	elif event.key==pygame.K_p and not stats.game_active:
		start_game(ai_settings,screen,stats,sb,ship,aliens,bullets)
	elif event.key==pygame.K_RIGHT:
		# 向右移动飞船
		ship.moving_right=True
	elif event.key==pygame.K_LEFT:
		# 向左移动飞船
		ship.moving_left=True
	elif event.key==pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)

def check_keyup_events(event,ship):
	if event.key==pygame.K_RIGHT:
		ship.moving_right=False
	elif event.key==pygame.K_LEFT:
		ship.moving_left=False

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
	"""单击Play开始"""
	button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		start_game(ai_settings,screen,stats,sb,ship,aliens,bullets)

def start_game(ai_settings,screen,stats,sb,ship,aliens,bullets):
	# 重置游戏统计信息
	stats.reset_stats()
	stats.game_active=True

	# 重置游戏设置
	ai_settings.initialize_dynamic_settings()

	# 重置各种分数
	sb.prep_score()
	sb.prep_high_score()
	sb.prep_level()
	sb.prep_ships()

	# 清空外星人和子弹
	aliens.empty()
	bullets.empty()

	# 创建新外星人，飞船居中
	create_fleet(ai_settings,screen,ship,aliens)
	ship.center_ship()

	# 隐藏光标
	pygame.mouse.set_visible(False)

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
	"""监听事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type==pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y=pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
		elif event.type==pygame.KEYDOWN:
			# 每个事件都只和一个按键关联
			# 同时按左右视为2个事件
			check_keydown_events(event,ai_settings,screen,stats,sb,ship,aliens,bullets)
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
	"""更新屏幕图像切换到新屏幕"""
		
	# 每次循环重绘屏幕
	screen.fill(ai_settings.bg_color)
	# 在飞船和外星人后面重绘所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	# 绘制飞船
	ship.blitme()

	# 绘制alien
	aliens.draw(screen)

	# score
	sb.show_score()

	# 如果游戏暂停,绘制Play
	if not stats.game_active:
		play_button.draw_button()

	# 让最新绘制的屏幕可见
	pygame.display.flip()	

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
	# 检查子弹击中alien,击中则删除
	# collisions是一个dict:key=bullet value=alien,True=delete
	collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)

	if collisions:
		# 要将每个击落的alien都计入得分
		for aliens in collisions.values():
			stats.score+=ai_settings.alien_points
			sb.prep_score()
		check_high_score(stats,sb)

	if len(aliens)==0:
		# 删除现有子弹并新建alien
		# 相当于一关结束刷新一遍
		bullets.empty()
		ai_settings.increase_speed()
		# 提高等级
		stats.level+=1
		sb.prep_level()
		create_fleet(ai_settings,screen,ship,aliens)

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""更新子弹位置删除消失的子弹"""
	bullets.update()

	# 删除消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)
	# 测试子弹确实被删除
	# 输出写入terminal比绘制图形还慢
	#print(len(bullets))
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
	"""alien hit ship"""

	if stats.ships_left > 0:
		stats.ships_left-=1

		# 更新ship图像
		sb.prep_ships()

		# clear aliens&bullets
		aliens.empty()
		bullets.empty()

		# 创建new alien & 重置ship到中央
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

		sleep(0.5)
	else:
		stats.game_active=False
		# 游戏结束后光标可见
		pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
	screen_rect=screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 和飞船碰撞一样处理
			ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
			break

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
	check_fleet_edges(ai_settings,aliens)
	aliens.update()

	"""检测alien&ship的碰撞"""
	if pygame.sprite.spritecollideany(ship,aliens):
		#### 这里可以改进为爆炸动画
		ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
	"""检测alien到底部"""
	check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)

def fire_bullet(ai_settings,screen,ship,bullets):
	# 创建子弹加入编组
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def get_number_aliens_x(ai_settings,alien_width):
	"""计算一行可以容纳的alien个数"""
	available_space_x=ai_settings.screen_width-(2*alien_width)
	number_alien_x=available_space_x//(2*alien_width)
	return number_alien_x

def get_number_rows(ai_settings,ship_height,alien_height):
	"""计算可以容纳的aliena行数"""
	available_space_y=ai_settings.screen_height-ship_height-3*alien_height
	number_rows=available_space_y//(2*alien_height)
	return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	# 在一行中创建单个alien
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien.x=alien_width+2*alien_width*alien_number
	alien.rect.x=alien.x
	alien.rect.y=alien.rect.height*(2*row_number+1)
	aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
	"""创建外星人群"""
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	number_alien_x=get_number_aliens_x(ai_settings,alien_width)
	number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

	for row_number in range(number_rows):
	# 创建一行alien
		for alien_number in range(number_alien_x):
			# 让外星人随机出现
			if randint(0,1):
				create_alien(ai_settings,screen,aliens,alien_number,row_number)

def change_fleet_direction(ai_settings,aliens):
	"""改变移动方向并且下移"""
	for alien in aliens.sprites():
		alien.rect.y+=ai_settings.fleet_drop_speed
	ai_settings.fleet_direction*=-1

def check_fleet_edges(ai_settings,aliens):
	"""有外星人到达边缘"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def check_high_score(stats,sb):
	if stats.score > stats.high_score:
		stats.high_score=stats.score
		sb.prep_high_score()