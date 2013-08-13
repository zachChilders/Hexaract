#! /usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabsstop=4

import pygame
import random

SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = 800, 640
FRAME_RATE = 30
SPEED = 4
ENEMIES_MAX = 10
BULLETS_MAX = 10
BULLET_DELAY = 7

class Character(pygame.sprite.Sprite):
	 #each class needs __init__ constructor

	def __init__(self, type_ = "player"): #self is this
		pygame.sprite.Sprite.__init__(self)
		self.type = type_
		self.x = self.y = 0
		self.x_increment = self.y_increment = 0
		self.image = pygame.image.load("%s.png" % self.type)
		self.width, self.height = self.image.get_size()
		self.speed = SPEED
		self.rect = self.image.get_rect()
		self.radius = self.width / 2
		self.rect.center = (self.x + (self.width / 2), self.y + (self.height /2))
		self.health = 1

	def update(self):
		self.x += self.x_increment
		self.y += self.y_increment
		self.rect.center = (self.x + (self.width / 2), self.y + (self.height /2))

	def draw(self, screen_):
		screen_.blit(self.image, (self.x, self.y))


class Player(Character):

	def __init__(self, x_ = 0, y_ = 0):
		Character.__init__(self, "player")
		self.x = x_
		self.y = y_
		self.health = 3
		self.bullets = pygame.sprite.Group()		
		self.bullet_delay = 0		
		self.score = 0

	def update(self):
		Character.update(self)
        	self.rect.center = (self.x + (self.width / 2), self.y + (self.height /2))

		if self.x < 0:
			self.x = 0
		elif self.x > SCREEN_WIDTH - self.width:
			self.x = SCREEN_WIDTH - self.width
		if self.y < 0:
			self.y = 0
		elif self.y > SCREEN_HEIGHT - self.height:
			self.y = SCREEN_HEIGHT - self.height
		
		if self.health <= 0:
			game_over = True

		self.bullets.update()
		for bullet in self.bullets:
			if bullet.x > SCREEN_WIDTH:
				self.bullets.remove(bullet)
		if self.bullet_delay > 0:
			self.bullet_delay -= 1
		
	def get_inputs(self):
		quit = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					quit = True
				if event.key == pygame.K_UP:
					self.y_increment = -self.speed
   				elif event.key == pygame.K_DOWN:
					self.y_increment = self.speed
				if event.key == pygame.K_LEFT:
					self.x_increment = -self.speed
				elif event.key == pygame.K_RIGHT:
					self.x_increment = self.speed
				elif event.key == pygame.K_SPACE:
					self.shoot()
			elif event.type == pygame.KEYUP:
				if event.key in [pygame.K_UP, pygame.K_DOWN]:
					self.y_increment = 0 
				elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
					self.x_increment = 0
		return quit

	def reset(self):
        	self.x = (SCREEN_WIDTH - player.width) / 2
		self.y = (SCREEN_HEIGHT - player.height) / 2	

	def shoot(self):
		if self.bullet_delay <= 0 and len(self.bullets) < BULLETS_MAX:
			new_bullet = Character("bullet")
			new_bullet.speed = 2 * self.speed
			new_bullet.x = self.x
			new_bullet.y = self.y + (self.height / 2)
			new_bullet.x_increment = new_bullet.speed
			self.bullets.add(new_bullet)
	
	def draw(self, game_screen):
		for bullet in self.bullets:
			bullet.draw(game_screen)
		Character.draw(self, game_screen)

class Enemy(Character):
	
	def __init__(self, type_):
		Character.__init__(self, type_) 
		Character.speed = SPEED / 2 
		self.x_increment = -self.speed
		self.score = 100

	def update(self):
		Character.update(self)
		if self.x < -self.width:
			self.kill()	

	def reset(self):
		self.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH * 2)
		self.y = random.randint(0, SCREEN_HEIGHT - self.height)


class MovableThing(pygame.sprite.Sprite):

	def __init__(self, type_):
		self.type = type_
		self.x = 0
		self.y = 0
		self.image = pygame.image.load("%s.png" % self.type)
		self.x_increment = -SPEED / 2
		self.y_increment = 0
		self.width, self.height = self.image.get_size()

	def update(self):
                self.x += self.x_increment
                self.y += self.y_increment

        def draw(self, screen_):
                screen_.blit(self.image, (self.x, self.y))


class Background(MovableThing):
	
	def __init__(self, type_):
		MovableThing.__init__(self, "background")
			
	def update(self):
		MovableThing.update(self)
		if self.x <= -self.width:
			self.reset()
	
	def reset(self):
		self.x = SCREEN_WIDTH - 1


class Bullet(Character):

	def __init__(self, Character_):
		MovableThing.__init__(self, "bullet")
		self.x = Character_.width
		self.y = Character_.height - Character_.height / 2
		self.x_increment = SPEED * 2
		self.y_increment = 0		

	def update(self):
		MovableThing.update(self)
		if self.x == SCREEN_WIDTH + self.x:
			return True
		else:
			return False
	
if __name__ == "__main__":

	pygame.init()
	
	game_screen = pygame.display.set_mode(SCREEN_SIZE)
	game_clock = pygame.time.Clock()
	game_over = False
	
	player = Player()
	player.x = (SCREEN_WIDTH - player.width) / 2
	player.y = (SCREEN_HEIGHT - player.height) / 2
	
	enemies = pygame.sprite.Group()
	
	backgrounds = []

	font = pygame.font.SysFont("monospace", 15)
	

	while not game_over:

		#Get user input
		game_over = player.get_inputs()
	
		while len(enemies) < ENEMIES_MAX:
			new_enemy = Enemy("enemy")
			new_enemy.reset()
			enemies.add(new_enemy)

		if len(backgrounds) <= 2:
			if len(backgrounds) == 0:
				new_background = Background("background")
				backgrounds.append(new_background)
			else:
				new_background = Background("background")
				background.x = SCREEN_WIDTH - 1
				backgrounds.append(new_background)

		#Update Background
		for background in backgrounds:
			background.update()	

		#Update player
		player.update()

		#Update all enemies
		enemies.update()
			
		#Check collisions		
		enemies_hit = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)

		for enemy in enemies_hit:
			player.health -= enemy.health
		#bullet collisions
		collision_dict = pygame.sprite.groupcollide(player.bullets, enemies, True, False)
		bullets_hit = collision_dict.keys()
		for bullet in bullets_hit:
			enemies_hit = collision_dict[bullet]
			for enemy in enemies_hit:
				enemy.health -= bullet.health
				if enemy.health <= 0 and enemies.has(enemy):
					enemies.remove(enemy)
					player.score += enemy.score

		#Draw things
		for background in backgrounds:
			background.draw(game_screen)
		player.draw(game_screen)

		for enemy in enemies:
			enemy.draw(game_screen)
		
		score = font.render("Score: " + str(player.score), True, (0,0,255))
		game_screen.blit(score, (0, SCREEN_HEIGHT))

		pygame.display.flip()
		game_clock.tick(FRAME_RATE)
		
	pygame.quit()
