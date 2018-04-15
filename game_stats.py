#coding=utf-8

class GameStats():
	"""跟踪游戏的统计活动"""

	def __init__(self, ai_settings):
		"""初始化统计数据"""
		self.ai_settings = ai_settings
		self.reset_stats()
		#游戏刚启动是处于不活跃状态
		self.game_active = False
	def reset_stats(self):
		"""初始化在游戏运行期间可能变化的信息"""
		self.ship_left = self.ai_settings.ship_limit