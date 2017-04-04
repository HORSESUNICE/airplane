class Settings():
	"""存储游戏设置"""

	def __init__(self):
		"""初始化游戏的静态设置"""
		self.screen_width=1200
		self.screen_height=800
		self.bg_color=(230,230,230)

		# 飞船设置
		self.ships_limit=3

		# 子弹设置
		self.bullet_width=300
		self.bullet_height=15
		# 这里颜色设置tuple也可以(60,60,60)
		self.bullet_color=60,60,60
		self.bullets_allowed=5

		# alien设置
		self.alien_speed_factor=10
		self.fleet_drop_speed=150
		# fleet_direction: r=1,l=-1
		self.fleet_direction=1

		# 以什么样的速度加快游戏节奏
		self.speedup_scale=1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""初始化游戏进行会改变的设置"""
		self.ship_speed_factor=100
		self.bullet_speed_factor=10
		self.alien_speed_factor=1

		# fleet_direction: r=1,l=-1
		self.fleet_direction=1

		# 游戏进行提高alien得分
		self.alien_points=50

	def increase_speed(self):
		"""提高游戏速度和alien分值"""
		self.ship_speed_factor*=self.speedup_scale
		self.bullet_speed_factor*=self.speedup_scale
		self.alien_speed_factor*=self.speedup_scale

		self.alien_points=int(self.alien_points*self.speedup_scale)