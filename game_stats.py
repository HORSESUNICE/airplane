class GameStats():
	"""游戏统计信息"""
	def __init__(self,ai_settings):
		"""初始化信息"""
		self.ai_settings=ai_settings
		self.reset_stats()
		# game运行为True
		# play游戏开始
		self.game_active=False
		# 任何情况都不会重置最高得分
		#### 这里还可以将历史最高分设置进来
		self.high_score=0

	def reset_stats(self):
		"""初始化游戏可能变化的信息"""
		self.ships_left=self.ai_settings.ships_limit
		# 在reset重置得分而不是在构造函数初始化
		self.score=0
		self.level=1