from __future__ import division

import pygame
from pygame.locals import *

class Console:
	def __init__(self, root):
		self.root = root
		self.root.console = self
	
		self.active = False
		self.show = False
		self.defColor = (40, 40, 40)
		self.color = (40, 40, 40)
		self.string = ""
		self.prefix = ">"
		self.refreshImgText(self.prefix+self.string, self.color)
		
		self.showResult = False
		self.successColor = (0, 255, 0)
		self.failColor = (255, 0, 0)
		self.resultTimer = 0
		self.showResTime = 80
		
		self.lastToggled = 0
		self.refireToggle = 20
		
		self.typeKeys = {K_a:"a", K_b:"b", K_c:"c", K_d:"d", K_e:"e", K_f:"f", K_g:"g", K_h:"h", K_i:"i", K_j:"j", K_k:"k", K_l:"l", K_m:"m", K_n:"n", K_o:"o", K_p:"p", K_q:"q", K_r:"r", K_s:"s", K_t:"t", K_u:"u", K_v:"v", K_w:"w", K_x:"x", K_y:"y", K_z:"z", K_BACKSPACE:"", K_RETURN:""}
		self.lastTyped = {}
		self.refireType = 10
	
	def refreshImgText(self, string, color):
		self.imgText = self.root.sysFont.render(string, 0, color)
	
	def update(self):
		if self.root.toggleConsole and not self.lastToggled:
			self.active = not self.active
			self.lastToggled = self.refireToggle
		
		if self.lastToggled > 0:
			self.lastToggled -= 1
		
		if self.active:
			if self.resultTimer>0:
				self.resultTimer = 0
				self.string = ""
				
				self.showResult = False
				self.color = self.defColor
			
			key = pygame.key.get_pressed()
			for x in self.typeKeys.keys():
				if key[x]:
					try:
						new = self.lastTyped[x] == 0
					except:
						new = True
						
					if new:
						#print x
						if x == 8: #backspace
							if len(self.string)>0:
								self.string = self.string[:-1]
						elif x == 13: #enter
							cmd = self.string
							result = self.command(cmd)
							
							if result[0]:
								self.string = " ".join(["Command",cmd,"executed successfully!",result[1]])
								self.color = self.successColor
							else:
								self.string = " ".join(["Command",cmd,"failed.",result[1]])
								self.color = self.failColor
							
							self.active = False
							self.showResult = True
							self.resultTimer = self.showResTime
						else:
							self.string = self.string+self.typeKeys[x]
						self.lastTyped[x] = self.refireType
			for key in self.lastTyped.keys():
				if self.lastTyped[key] > 0:
					self.lastTyped[key] -= 1
			self.refreshImgText(self.prefix+self.string, self.color)
		elif self.showResult:
			self.resultTimer -= 1
			if self.resultTimer == 0:
				self.showResult = False
				self.color = self.defColor
			self.refreshImgText(self.prefix+self.string, self.color)
		else:
			self.string = ""
			self.refreshImgText("", self.color)
		
		self.show = self.active or self.showResult
	
	def command(self, string):
		self.active = False
		
		if string == "noclip":
			player = self.root.Myself
			player.noclip = not player.noclip
			if self.root.Myself.noclip:
				return (True, "Noclip on.")
			else:
				return (True, "Noclip off.")
		else:
			return (False, "")
	
#print(", ".join(["".join(['K_',chr(x),':"',chr(x), '"']) for x in range(97, 123)]))