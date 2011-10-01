from __future__ import division

import pygame
from pygame.locals import *
from collision import characterHitObstacle, objectCheckCollision
from gameobject import GameObject
from functions import sign, place_free, point_direction, load_image
from weapons import Weapon, ScatterGun

class Character(GameObject):
	def __init__(self, root):
		GameObject.__init__(self, root, 0, 0)
		self.flip = 0
		self.onGround = False
		self.noclip = False
		self.noclip = True
		
		self.maxJumps = 1
		self.currentJumps = 0
		
		self.accel = 1000
		self.moveSpeed = 120
		self.jumpForce = 200 #was 80
		
		#this should be based on the game, not on the character
		self.gravity = 400 #was 100
		#self.gravityOverride for gameobjects?
		
	def step(self, frametime):
		if not self.root.console.active:
			if self.root.left: self.hspeed -= self.accel * frametime
			if self.root.right: self.hspeed += self.accel * frametime
			
			if self.root.up:
				if self.onGround or self.noclip:
					self.vspeed = -self.jumpForce
		
		if not (self.root.left or self.root.right) or self.root.console.active:
			if abs(self.hspeed) < 10: self.hspeed = 0
			else: self.hspeed -= sign(self.hspeed) * min(abs(self.hspeed), self.moveSpeed * frametime)
		
		# gravitational force
		self.vspeed += self.gravity * frametime

		# TODO: air resistance, not hard limit
		self.vspeed = min(self.gravity, self.vspeed)
		self.hspeed = min(self.moveSpeed, max(-self.moveSpeed, self.hspeed))


	def endStep(self, frametime):
		GameObject.endStep(self, frametime)
		self.weapon.posUpdate()

	def collide(self, frametime):
		check = objectCheckCollision(self)
		
		if check: characterHitObstacle(self, frametime)

		GameObject.collide(self, frametime)


	def draw(self):
		mouse_x, mouse_y = pygame.mouse.get_pos()

		if point_direction(self.x, self.y, mouse_x + self.root.Xview, mouse_y + self.root.Yview) > 90 and point_direction(self.x, self.y, mouse_x + self.root.Xview, mouse_y + self.root.Yview) < 270:
			if self.flip == 0:
				self.sprite = pygame.transform.flip(self.sprite, 1, 0)
				self.flip = 1
		else:
			if self.flip:
				self.sprite = pygame.transform.flip(self.sprite, 1, 0)
				self.flip = 0

		GameObject.draw(self)



class Scout(Character):
	def __init__(self, root):
		Character.__init__(self, root)

		self.sprite = load_image("sprites/characters/scoutreds/0.png")

		# The Scout hitbox: left = -6; right = 6; top = -10; bottom = 23
		self.rect = pygame.Rect(self.x - 6, self.y - 10, 12, 33)

		self.xImageOffset = 30
		self.yImageOffset = 40

		self.hp = 100
		self.maxHp = 100

		self.moveSpeed = 200
		
		self.weapon = ScatterGun(self.root, self.x, self.y)
		self.weapon.owner = self

		self.xRectOffset = self.x - self.rect.centerx
		self.yRectOffset = self.y - self.rect.centery
